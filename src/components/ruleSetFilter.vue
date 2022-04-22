<template>
  <div style="padding: 4px;">
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
  props: ["rowData"],
  data: () => ({
    // rowData: this.rowData,
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
    paramsListChange: [],
    headers: [
      {
        text: "Name",
        value: "name",
      },
    ],
  }),
  beforeMount() {
    console.log("rowData");
    console.log(this);
    this.initData();
  },

  watch: {
    selected: function() {
      console.log("selected");
      this.updateFilter();
    },
    paramsListChange: function() {
      // this.initData();
      console.log("fullList updated");
      this.updateFilter();
    },
  },
  methods: {
    initData() {
      console.log("before mount");
      console.log("props");
      console.log(this.params.rowModel.gridApi);
      this.data = {};
      // let paramsList = this.params.api
      //   .getModel()
      //   .rowsToDisplay.map((element) => element.data.NAME);
      let paramsList = [];
      this.params.rowModel.gridApi.forEachNode((node) =>
        paramsList.push(node.data.NAME)
      );
      // console.log(paramsList);
      // console.log(this.params.rowModel.gridApi);
      this.data.fullList = paramsList.map((elem) => ({ name: elem }));
      this.selected = this.data.fullList;
      this.paramsListChange = paramsList;
    },
    updateFilter() {
      console.log("update filter");
      //forEachNode(node => console.log(node.data.NAME))
      this.params.filterChangedCallback();
    },
    destroyFilter() {
      console.log("destroy filter");
      this.gridApi.destroyFilter("NAME");
    },
    doesFilterPass(params) {
      let flatten = this.selected.map((elem) => elem.name);
      // console.log("params");
      // console.log(params);
      // console.log(flatten);
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
