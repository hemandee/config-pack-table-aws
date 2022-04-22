<template>
  <div class="tooltip">
    <p>{{ data }}</p>
  </div>
</template>
<script>
export default {
  name: "customTooltip",
  data: () => ({ data: null }),
  beforeMount() {
    if (this.params.value == "X") {
      this.data = this.params.column.getColId() || "Empty";
    } else {
      this.data = this.params.value;
    }
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
