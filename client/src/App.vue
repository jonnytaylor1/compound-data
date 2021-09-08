<template>
  <div id="app">
    <Graphs/>
  </div>
</template>

<script>
import Graphs from './components/Graphs.vue';

export default {
  components: { Graphs },
};
</script>

<style>

p, ul, li {
    padding: 0;
    margin: 0;
}

li, p, h1, h2, h3 {
  font-family:Verdana, Geneva, Tahoma, sans-serif
}
li {
  list-style: none;
}

</style>