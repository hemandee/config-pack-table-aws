<template>
  <div style="display: flex; flex-direction: column; height: 100%">
    <v-dialog :value="missingRulesDialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          New Rules not in Config Packs
        </v-card-title>

        <v-card-text>
          <div class="missing_rules_columns">
            Updated {{ version.date }}
            <div v-for="(item, index) in missingRules" :key="index">
              {{ item }}
            </div>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="missingRulesDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-row>
      ><v-col>
        <v-btn @click="downloadCSV">
          <v-icon large>
            mdi-export
          </v-icon>
          Export to CSV
        </v-btn>

        <template>
          <v-btn @click="missingRulesDialog = true">
            New Rules
          </v-btn>
        </template>
      </v-col>
    </v-row>
    <ag-grid-vue
      style="width: 100%; height: 100%"
      class="ag-theme-alpine"
      :columnDefs="headers"
      :rowData="data"
      @grid-ready="onGridReady"
      rowDragManaged="true"
      animateRows="true"
      debug="false"
      tooltipShowDelay="0"
      :defaultColDef="defaultColDef"
      tooltipMouseTrack="true"
    >
    </ag-grid-vue>
  </div>
</template>

<script>
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import { VDataTable, VSwitch } from "vuetify/lib/components";

import { AgGridVue } from "ag-grid-vue";
import data_rules from "../assets/data.json";
import data_headers from "../assets/data_headers.json";
import version from "../assets/VERSION.json";
export default {
  name: "App",
  data: () => ({
    columns: [{ prop: "NAME", name: "NAME", size: 300, pin: "colPinStart" }],
    rows: [{ name: "1", details: "Item 1" }],
    data: [],
    gridApi: null,
    defaultColDef: {
      tooltipComponent: "customTooltip",
      resizeable: true,
    },
    missingRules: ["Empty"],
    missingRulesDialog: false,
    version: version,
  }),
  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.parsePacks();
    },
    parsePacks(packs) {
      this.log("Parsing Config Packs", packs);
      this.data = [...data_rules];
      this.parseHeaders();
    },
    parseHeaders() {
      let headers = {};
      let all_headers = this.data.flatMap((x) => Object.keys(x));
      headers = [...new Set(all_headers)];
      this.missingRules = data_headers.filter((x) => !headers.includes(x));
      this.genHeaders(headers);
      this.log("Completed Table Generation");
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    genHeaders(headers) {
      this.log("Generating Columns Names");
      let columns = [];
      for (let item in headers) {
        columns.push({
          //   prop: headers[item],
          field: headers[item],
          sortable: false,
          filter: true,
          tooltipField: headers[item],
        });
      }
      const isName = (element) => element.field == "NAME";
      const isToalCount = (element) => element.field == "TOTAL_RULES";
      columns.splice(columns.findIndex(isName), 1);
      columns.splice(columns.findIndex(isToalCount), 1);

      columns.push({
        field: "NAME",
        pinned: "left",
        rowDrag: true,
        lockPinned: false,
        filterFramework: "ruleSetFilter",
        width: 300,
      });
      columns.push({
        field: "TOTAL_RULES",
        pinned: "left",
        rowDrag: false,
        lockPinned: false,
        width: 130,
        sortable: true,
      });
      this.headers = columns;
    },

    log(message) {
      let msg = `${new Date(Date.now()).toLocaleTimeString()} :  ${message}`;
      this.logMsg = msg;
      console.log(message);
    },
    downloadCSV() {
      this.gridApi.exportDataAsCsv();
    },
  },
  components: {
    "ag-grid-vue": AgGridVue,
    // eslint-disable-next-line vue/no-unused-components
    ruleSetFilter: {
      template: `
      <div style="padding: 4px; width: 220px;">
      <div style="font-weight: bold;">Rule Set</div>

      <div>
      <v-data-table
      v-model="selected"
      :items="data.fullList"
      :single-select="singleSelect"
      show-select
      class="elevation-1"
      item-key=name
      :headers="headers"
      :hide-default-header=hideHeaders
      :items-per-page=itemspage
      :hide-default-footer=hidefooter
    >
      </template>
    </v-data-table>
      </div>
      </div>
    `,

      components: { VDataTable, VSwitch },
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
    },
    // eslint-disable-next-line vue/no-unused-components
    customTooltip: {
      template: `
      <div class="tooltip">
          <p>{{ data }}</p>
      </div>
    `,
      data: function() {
        return null;
      },
      beforeMount() {
        this.data = this.params.column.getColId() || "Empty";
        console.log(this.data);
      },
    },
  },
};
</script>
<style>
.tooltip {
  position: absolute;
}

.tooltip.ag-tooltip-hiding {
  opacity: 0;
}

.tooltip p {
  font-weight: bold;
  background-color: skyblue;
}
</style>
