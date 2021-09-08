<template>
<Graph graph="scatter" :scatterData="assay[category]" :xLabels="xLabels" :yLabels="yLabels" yTitle="Inhibition (%)" xTitle="Concentration (M)" />
</template>

<script>
import Graph from './Graph.vue';

export default {
    components: {
        Graph
    },
    props: {
        category: String,
    },
    watch: {
        category: {
            handler() {this.fetchAssay()},
            immediate: true
        }
    },
    mounted() {
        this.fetchAssay()
    },
    methods: {
        async fetchAssay() {
            if (!this.assay[this.category]) {
                const res = await this.$http.get(`http://localhost:5000/assay/${this.category}`);
                this.$set(this.assay, this.category, res.data)
            }
        },
        expo(x, f) {
            return Number.parseFloat(x).toExponential(f);
        }
    },
    data: () => ({
        assay: {},
        yLabels: [0, 25, 50, 75, 100]
    }),
    computed: {
        selectedAssay() {
            return this.assay[this.category]
        },
        xLabels() {
            if (this.selectedAssay) return [...new Set(this.selectedAssay.map(c => c.assay.map(a => a.concentration)).flat())].sort((a, b) => a - b).map(label => this.expo(label, 1))
        },
    },
};
</script>