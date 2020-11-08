<template>
  <div id="app">
    <section class="hero is-primary is-info">
      <navbar />
    </section>
    <section class="hero-body">
        <router-view/>
    </section>
  </div>
</template>

<script>
import Navbar from "@/components/ui/Navbar.vue"

export default {
  name: 'App',
  components: {
    Navbar,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
