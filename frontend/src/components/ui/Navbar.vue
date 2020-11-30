<template>
<!--  <div class="hero-head"> -->
  <nav role="navigation" class="navbar is-fixed-top is-dark">
        <div class="navbar-brand">
          <a href="/" class="navbar-item router-link-exact-active router-link-active"
          ><img src="https://i.imgur.com/8ZbVsyK.png" style="max-height: 48px;"/></a>
        </div>
        <div class="navbar-menu">
          <div class="navbar-start">
            <p class="navbar-item subtitle" >Phishpond</p>
          </div>
          <div class="navbar-end">
              <router-link class="navbar-item" to="/home">
                Home
              </router-link>
          </div>
        </div>
    </nav>
<!--  </div>-->
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
