<template>
<Graph graph="line" :xLabels="xLabels" :yLabels="yLabels" xTitle="Assay Result Label" yTitle="IC50 (M)" :lineData="ic50ByLabel" />
</template>

<script>
import Graph from './Graph.vue'
export default {
    components: {
        Graph
    },
    async beforeCreate () {
        const res = await this.$http.get(`http://localhost:5000/ic50_label`)
        this.ic50ByLabel = res.data
    },
    data: () => ({
        ic50ByLabel: null,
        ticks: 4
    }),
    methods: {
        strip(number) {
            return parseFloat(parseFloat(number).toPrecision(12).toString())
        },
        niceNum(range, round) {
            const exponent = Math.floor(Math.log10(range));
            const fraction = range / Math.pow(10, exponent);
            let niceFraction
            if (round) {
                if (fraction < 1.5)
                    niceFraction = 1;
                else if (fraction < 3)
                    niceFraction = 2;
                else if (fraction < 7)
                    niceFraction = 5;
                else
                    niceFraction = 10;
            } else {
                if (fraction <= 1)
                    niceFraction = 1;
                else if (fraction <= 2)
                    niceFraction = 2;
                else if (fraction <= 5)
                    niceFraction = 5;
                else
                    niceFraction = 10;
            }
            return niceFraction * Math.pow(10, exponent);
        }
    },
    computed: {
        xLabels() {
            if (this.ic50ByLabel) return Object.keys(this.ic50ByLabel).map(key => {
                return key.split('_').map(w => {
                    return w.charAt(0).toUpperCase() + w.slice(1);
                }).join(' ')
            })
        },
        niceLabels() {
            const range = this.niceNum(this.yMax - this.yMin, false);
            const increment = this.strip(this.niceNum(range / this.ticks, true));
            const min = this.strip(Math.floor(this.yMin / increment) * increment);
            const max = this.strip(Math.ceil(this.yMax / increment) * increment);
            return {
                min,
                max,
                increment
            }
        },
        yMin() {
            return Math.min(...this.yData)
        },
        yMax() {
            return Math.max(...this.yData)
        },
        //suitable y axis labels
        yLabels() {
            const arr = []
            for (let i = this.niceLabels.min; i <= this.niceLabels.max; i += this.niceLabels.increment) {
                arr.push(this.strip(i))
            }
            return arr
        },
        //all y data points
        yData() {
          if (this.ic50ByLabel) {
            return Object.keys(this.ic50ByLabel).reduce((a, l) => {
                return a.concat(this.ic50ByLabel[l])
            }, []).reduce((a, c) => {
                return a.concat(c.ic50)
            }, [])
          }
          else return []
        }
    }
}
</script>
