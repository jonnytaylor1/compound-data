<template>
<div>
    <GraphLegend :labels="legend" />
    <div class="container">
        <svg viewBox="0 0 330 220">
            <line :x1="minXPosition" :x2="minXPosition" :y1="minYPosition" :y2="maxYPosition" :stroke="lineColor" :stroke-width="lineWidth" />
            <line :stroke-width="lineWidth" :x1="minXPosition" :x2="maxXPosition" :y1="minYPosition" :y2="minYPosition" :stroke="lineColor" />
            <text class="title" :x="minXPosition - 50" :y="yTitlePosition">{{yTitle}}</text>
            <text class="title" text-anchor="middle" :y="minYPosition + 20" :x="xTitlePosition">{{xTitle}}</text>
            <template v-for="(label, i) in xLabels">
                <text :key="`xlabel${label}`" text-anchor="middle" :x="xLabelPosition(i)" :y="minYPosition + 10">{{label}}</text>
                <line :key="`xtick${label}`" :x1="xLabelPosition(i)" :x2="xLabelPosition(i)" :y1="minYPosition" :y2="minYPosition + 2" :stroke="lineColor" :stroke-width="lineWidth" />
            </template>
            <template v-for="(label, i) in yLabels">
                <text :key="`ylabel${label}`" text-anchor="end" :y="yLabelPositions[i]" :x="minXPosition - 10">{{label}}</text>
                <line :key="`ytick${label}`" :x1="minXPosition - 2" :x2="minXPosition" :y1="yLabelPositions[i]" :y2="yLabelPositions[i]" :stroke="lineColor" :stroke-width="lineWidth" />
            </template>
            <template v-if="graph === 'line'">
                <template v-for="(ic50Array, category, i) in lineMappedData">
                    <circle v-for="(ic50, j) in ic50Array" :key="`plot${j}${category}`" :cx="xLabelPosition(i)" :cy="position(ic50.ic50, yLabels[0], yLabels[yLabels.length -1], maxYPosition, minYPosition)" r="1" :fill="ic50.color" />
                </template>
            </template>
            <template v-else-if="graph === 'scatter'">
                <template v-for="compound in scatterMappedData">
                    <template v-for="(assay, i) in compound.assay">
                        <circle :key="`plot${i}${compound.id}`" :cx="assay.x" :cy="assay.y" r="1" :fill="compound.color" />
                        <line v-if="i !== 0" :key="`line${i}${compound.id}`" :x1="compound.assay[i-1].x" :x2="assay.x" :y1="compound.assay[i-1].y" :y2="assay.y" :stroke="compound.color" :stroke-width="lineWidth" />
                    </template>
                </template>
            </template>

        </svg>
    </div>
</div>
</template>

<script>
import colors from '@/utils/colors.js'
import GraphLegend from './GraphLegend.vue'
export default {
    components: {
        GraphLegend
    },
    props: {
        scatterData: Array,
        lineData: Object,
        xLabels: Array,
        yLabels: Array,
        yTitle: String,
        xTitle: String,
        graph: {
            type: String,
            validator: value => (['scatter', 'line'].includes(value))
        }
    },
    data: () => ({
        maxYPosition: 5,
        minYPosition: 195,
        maxXPosition: 250,
        minXPosition: 50,
        lineWidth: '0.5',
        lineColor: 'black'
    }),
    methods: {
        xLabelPosition(index) {
            if (this.graph === 'scatter') {
                const xLabels = this.xLabels
                const label = xLabels[index]
                return this.position(label, Math.min(...xLabels), Math.max(...xLabels), this.maxXPosition, this.minXPosition)
            } else if (this.graph === 'line') {
                return (this.distanceBetweenX / 2) + this.minXPosition + this.distanceBetweenX * index
            }
        },
        position(value, min, max, positionMax, positionMin) {
            const positionRange = positionMax - positionMin
            const range = max - min
            const position = ((positionRange / range) * value) + positionMin - (positionRange * min / range)
            return position
        },
        labelPosition(labels, positionMax, positionMin) {
            return labels.map(label => this.position(parseFloat(label), Math.min(...labels), Math.max(...labels), positionMax, positionMin))
        },
    },
    computed: {
        yTitlePosition() {
            return 0.5 * (this.maxYPosition + this.minYPosition)
        },
        xTitlePosition() {
            return 0.5 * (this.maxXPosition + this.minXPosition)
        },
        distanceBetweenX() {
            const labelsFrequency = this.xLabels.length
            const range = this.maxXPosition - this.minXPosition
            return range / labelsFrequency
        },
        yLabelPositions() {
            return this.labelPosition(this.yLabels, this.maxYPosition, this.minYPosition)
        },
        lineMappedData () {
          let index = 0
            const mappedData = {}
            for (const category in this.lineData) {
                if (Object.hasOwnProperty.call(this.lineData, category)) {
                    const ic50Array = this.lineData[category];
                    const copy = ic50Array.map(ic50 => {
                        const obj = {
                            ...ic50,
                            color: colors[index]
                        }
                        index++
                        return obj
                    })
                    mappedData[category] = copy
                }
            }
            return mappedData
        },
        scatterMappedData () {
            if (this.scatterData) {
                return this.scatterData.map((obj, i) => ({
                    ...obj,
                    assay: obj.assay.map(a => ({
                        ...a,
                        x: this.position(a.concentration, Math.min(...this.xLabels), Math.max(...this.xLabels), this.maxXPosition, this.minXPosition),
                        y: this.position(a.inhibition, Math.min(...this.yLabels), Math.max(...this.yLabels), this.maxYPosition, this.minYPosition),
                    })),
                    color: colors[i]
                }))
            }
        },
        legend() {
            if (this.graph === 'scatter') return this.scatterMappedData
            else if (this.graph === 'line') {
                return Object.values(this.lineMappedData).flat().sort((a, b) => (a.id - b.id))
            }
        }
    }
}
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
}
text {
    font-size: 0.3rem;
}
.title {
    font-weight: bold;
}
svg {
    max-width: 60rem;
}

</style>
