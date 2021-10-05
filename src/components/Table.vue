<template>
  <div style="display: flex; flex-direction: column; height: 100%">
    <v-expansion-panels>
      <v-expansion-panel>
        <v-expansion-panel-header>
          <h4>
            How to Use
          </h4>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div>
            Features:
            <ul>
              <li>Drag by Name Columns</li>
              <li>Filter by list of Name (Disables Drag)</li>
              <li>Sort by TOTAL_RULES</li>
              <li>Filter each Rule contains by 'X'</li>
              <li>Extra Rule that are not in Conformance packs</li>
              <li>
                Export filtered table to csv for use in Excel or other
                applications
              </li>
            </ul>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-toolbar dense>
      <v-btn @click="downloadCSV">
        <v-icon large>
          mdi-export
        </v-icon>
        Export to CSV
      </v-btn>
      <v-spacer />
      <v-btn @click="missingRulesDialog = true">
        Extra Rules
      </v-btn></v-toolbar
    >

    <v-dialog :value="missingRulesDialog" width="500" fullscreen>
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Extra Rules not in Config Packs
          <v-btn color="primary" text @click="missingRulesDialog = false">
            Close
          </v-btn>
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
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-row>
      ><v-col>
        <template> </template>
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
import { AgGridVue } from "ag-grid-vue";
import data_rules from "../assets/data.json";
import data_headers from "../assets/data_headers.json";
import version from "../assets/VERSION.json";
import customTooltip from "./customTooltip";
import ruleSetFilter from "./ruleSetFilter";

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
    ruleSetFilter: ruleSetFilter,

    // eslint-disable-next-line vue/no-unused-components
    customTooltip: customTooltip,
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
