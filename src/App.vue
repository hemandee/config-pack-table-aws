<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      Config Pack Table
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
