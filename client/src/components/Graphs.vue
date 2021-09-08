<template>
<div>
    <Tabs :activeIndex="tabIndex" @changeIndex="tabIndex = $event" v-if="tabItems.length" :tabItems="tabItems" />
    <Tabs v-if="tabIndex === 0 && tabItems2.length" :activeIndex="tabIndex2" @changeIndex="tabIndex2 = $event" :tabItems="tabItems2" />
    <keep-alive>
        <AssayGraph :category="formattedCategory" v-if="type==='Assay Results'" />
        <IC50Graph v-else-if="type === 'IC50 and Label'" />
    </keep-alive>
</div>
</template>

<script>
import AssayGraph from './AssayGraph.vue'
import IC50Graph from './IC50Graph.vue';

import Tabs from './Tabs.vue'
export default {
    components: {
        AssayGraph,
        Tabs,
        IC50Graph
    },
    data: () => ({
        tabIndex: 0,
        tabItems: ['Assay Results', 'IC50 and Label'],
        tabIndex2: 0,
        tabItems2: ['Fragment Hit', 'Candidate', 'Probe', 'Starting Point'],
    }),
    computed: {
        category() {
            return this.tabItems2[this.tabIndex2]
        },
        type() {
            return this.tabItems[this.tabIndex]
        },
        formattedCategory() {
            return this.category.toLowerCase().replace(' ', '_')
        }
    }
}
</script>
