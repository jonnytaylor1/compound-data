<template>
<div class="legend">
    <button v-for="label in labels" :key="label.id" class="icon">
        <div class="circle" :style="`backgroundColor: ${label.color}`"></div>
        <p class="label">{{label.id}}</p>
    </button>
</div>
</template>

<script>
    export default {
        props: {
            labels: Array
        }
    }
</script>

<style scoped>
.legend {
    display: flex;
    flex-wrap: wrap;
    margin: 2rem auto;
    max-width: 45rem;
    gap: 1rem;
    border: solid black 1px;
    padding: 1rem;
    max-height: 1.25rem;
    overflow-y: auto;
}
.icon {
    display: flex;
    align-items: center;
}
.circle {
    height: 1rem;
    width: 1rem;
    background: yellow;
    border-radius: 1rem;
    border: 0.5px solid grey;
    margin-right: 0.25rem;
}
</style>