<template>
  <v-app>
    <v-app-bar app color="primary">
      <v-img
        max-height="50"
        max-width="70"
        alt="logo"
        src="./assets/binbuddy.png"
        dark
      ></v-img>
      <div>Digitaler Entsorgungskalender</div>
      <v-spacer></v-spacer>
      <v-col
        class="d-flex"
        cols="1"
      >
        <v-select
          :items="languages"
          label="Sprache"
        ></v-select>
      </v-col>
    </v-app-bar>

    <v-main>
      <HelloWorld />
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld";

export default {
  name: "App",

  components: {
    HelloWorld,
  },

  data: () => ({
    languages: ['DE', 'FR', 'IT', 'RT', 'EN'],
  }),
};
</script>
