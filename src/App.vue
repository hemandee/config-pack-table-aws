<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>
        Table of Managed Config Conformance Packs and included rules with Export
        to CSV and Filter Options</v-app-bar-title
      >
    </v-app-bar>

    <v-main>
      <Table />
    </v-main>
  </v-app>
</template>

<script>
import Table from "./components/Table";

export default {
  name: "App",

  components: {
    Table,
  },

  data: () => ({
    //
  }),
};
</script>
