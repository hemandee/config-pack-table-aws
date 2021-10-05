<template>
  <div style="padding: 4px; width: 220px;">
    <div style="font-weight: bold;">Rule Set</div>

    <div>
      <v-data-table
        v-model="selected"
        :items="data.fullList"
        :single-select="singleSelect"
        show-select
        class="elevation-1"
        item-key="name"
        :headers="headers"
        :hide-default-header="hideHeaders"
        :items-per-page="itemspage"
        :hide-default-footer="hidefooter"
      >
      </v-data-table>
    </div>
  </div>
</template>
<script>
export default {
  name: "ruleSetFilter",
  data: () => ({
    fullList: [
      {
        name: "CIS-AWS-FB-v1.3-Level1",
      },
      {
        name: "AWS-Well-Architected-Security-Pillar",
      },
    ],
    singleSelect: false,
    selected: [],
    hideHeaders: false,
    itemspage: -1,
    hidefooter: true,
    headers: [
      {
        text: "Name",
        value: "name",
      },
    ],
  }),
  beforeMount() {
    this.data = {};
    let paramsList = this.params.api
      .getModel()
      .rowsToDisplay.map((element) => element.data.NAME);
    this.data.fullList = paramsList.map((elem) => ({ name: elem }));
    this.selected = this.data.fullList;
  },

  watch: {
    selected: function() {
      this.updateFilter();
    },
  },
  methods: {
    updateFilter() {
      this.params.filterChangedCallback();
    },

    doesFilterPass(params) {
      let flatten = this.selected.map((elem) => elem.name);

      return flatten.includes(params.data.NAME);
    },

    isFilterActive() {
      console.log("filteractive");
      return (
        this.selected != null &&
        this.selected !== "" &&
        this.selected != this.fullList
      );
    },

    getModel() {
      console.log("getmodel");

      return { value: this.selected };
    },

    setModel(model) {
      console.log("setmodel");

      this.selected = model.value;
    },
  },
};
</script>
<style></style>
