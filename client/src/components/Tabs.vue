<template>
<ul>
    <li :class="[{'active' :activeIndex === index}]" @click="$emit('changeIndex', index)" v-for="(item, index) in tabItems" :key="item">{{item}}</li>
</ul>
</template>

<script>
export default {
    props: {
        tabItems: Array,
        activeIndex: Number
    }
}
</script>

<style scoped>
ul {
    display: flex;
    justify-content: center;
    margin: 0 auto;
    gap: 1rem;
    margin-bottom: 2rem;
}
li {
    color: rgb(64, 64, 64);
}

li:hover {
    cursor: pointer;
}

.active {
    font-weight: 700;
}
</style>
