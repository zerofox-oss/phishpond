<template>
  <div class="hero-head">
    <nav class="navbar">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" >Phishpond</a>
        </div>
        <div class="navbar-end">
            <router-link class="navbar-item" to="/home">
              Home
            </router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
    }
  }
}
</script>
<style>
.b-navbar {
  &.is-transparent {
    background-color: transparent;
    background-image: none;
  }
}
</style>
