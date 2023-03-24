<template>
  <v-app-bar app color="primary" dark>
    <v-app-bar-nav-icon> </v-app-bar-nav-icon>
    <v-toolbar-title>Digitaler Entsorgunskalender</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-menu left bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on">
          <v-icon>mdi-translate</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="language in languages"
          :key="language"
          @click="() => {}"
        >
          {{ language }}
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
export default {
  name: "Navigation",
  data: () => ({
    languages: ["DE", "FR", "IT", "RT", "EN"],
  }),
};
</script>
