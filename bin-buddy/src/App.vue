<template>
  <v-app>
    <Navigation />
    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld";
import Navigation from "./components/Navigation";

export default {
  name: "App",

  components: {
    HelloWorld,
    Navigation,
  },
};
</script>
