<template>
  <div id="app">
      <navbar />
      <section class="hero">
        <div class="hero-body">
          <div class="container">
            <router-view/>
          </div>
        </div>
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
body{
  padding-top: 0px!important;
}
</style>
