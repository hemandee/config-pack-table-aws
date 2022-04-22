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
              <li>Select Rows to generate template</li>
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
      <!-- <v-btn @click="toCF">
        <v-icon large>
          mdi-export
        </v-icon>
        Export to CF
      </v-btn> -->
      <v-spacer />
      <v-switch
        @change="flipColumnsTable"
        v-model="flipColumns"
        :loading="flipColumnsLoading"
      >
      </v-switch>
      <v-spacer />
      <v-btn @click="missingRulesDialog = true">
        Extra Rules
      </v-btn>
    </v-toolbar>

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
      :overlayLoadingTemplate="overlayLoadingTemplate"
      :rowMultiSelectWithClick="true"
      rowSelection="multiple"
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
import data_rule_set from "../assets/data_rule_set.json";
import customTooltip from "./customTooltip";
import ruleSetFilter from "./ruleSetFilter";
import cfinput from "../helper/genCloudformation";

const toolTipValueGetter = function(params) {
  return params.value || "X";
};

export default {
  name: "App",
  data: () => ({
    columns: [{ prop: "NAME", name: "NAME", size: 300, pin: "colPinStart" }],
    rows: [{ name: "1", details: "Item 1" }],
    data: [],
    gridApi: null,
    defaultColDef: {
      // tooltipComponent: "customTooltip",
      resizeable: true,
      tooltipValueGetter: toolTipValueGetter,
      tooltipComponentFramework: "customTooltip",
    },
    missingRules: ["Empty"],
    missingRulesDialog: false,
    version: version,
    flipColumns: true,
    flipColumnsLoading: false,
    overlayLoadingTemplate: null,
    rowSelection: null,
  }),
  created() {
    this.overlayLoadingTemplate =
      '<span class="ag-overlay-loading-center">Please wait while your rows are loading</span>';
    this.initialize();
  },

  methods: {
    initialize() {
      this.parsePacks();
    },
    toolTipValueGetter(params) {
      console.log(params);
      return { value: params.value };
    },
    rule_set() {
      this.log("Parsing Config Packs with Row RuleSet");
      // this.gridApi.showLoadingOverlay();
      this.data = [...data_rule_set];
      console.log(this.data_rule_set);
      this.parseHeaders(this.data);
    },
    parsePacks() {
      this.log("Parsing Config Packs");
      // this.gridApi.showLoadingOverlay();
      this.data = [...data_rules];
      this.parseHeaders(this.data);
    },
    parseHeaders(data) {
      let headers = {};
      let all_headers = data.flatMap((x) => Object.keys(x));
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

          resizable: true,
          tooltipValueGetter: toolTipValueGetter,
          tooltipComponentFramework: "customTooltip",
        });
      }
      const isName = (element) => element.field == "NAME";
      const isTotalCount = (element) => element.field == "TOTAL_RULES";
      const isURL = (element) => element.field == "URL";

      columns.splice(columns.findIndex(isName), 1);
      columns.splice(columns.findIndex(isTotalCount), 1);
      columns.splice(columns.findIndex(isURL), 1);

      columns.push({
        field: "NAME",
        pinned: "left",
        rowDrag: true,
        lockPinned: false,
        filterFramework: "ruleSetFilter",
        filterParams: {
          flipColumns: this.flipColumns,
        },
        width: 300,
        sortable: true,
        tooltipValueGetter: toolTipValueGetter,
      });
      if (this.flipColumns == true) {
        columns.push({
          field: "TOTAL_RULES",
          pinned: "left",
          rowDrag: false,
          lockPinned: false,
          width: 130,
          sortable: true,
        });
      }
      columns.push({
        field: "URL",
        pinned: "left",
        rowDrag: false,
        lockPinned: false,
        hide: true,
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
    toCF() {
      this.log("Cloudformation");
      cfinput(this.gridApi.getSelectedNodes(), this.flipColumns);
    },
    flipColumnsTable() {
      console.log(this.gridApi);
      // console.log(this.gridColumnApi);
      const filterinstance = this.gridApi.getFilterInstance("NAME");
      const vueFilterInstance = filterinstance.getFrameworkComponentInstance();

      this.data = "";
      console.log("flipcolumnsloading is", this.flipColumnsLoading);
      if (this.flipColumns) {
        this.flipColumnsLoading = true;
        console.log("default");
        this.parsePacks();
        // this.flipColumnsLoading = false;
      } else if (this.flipColumns == false) {
        this.flipColumnsLoading = true;
        console.log("flip columns");
        this.rule_set();
        // this.flipColumnsLoading = false;
        console.log(this.flipColumnsLoading);
      }
      console.log("start");
      console.log("flipcolumnsloading is", this.flipColumnsLoading);

      this.gridApi.showLoadingOverlay();
      setTimeout(() => {
        vueFilterInstance.initData();
        console.log("end");
        this.flipColumnsLoading = false;
      }, 1000);
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
