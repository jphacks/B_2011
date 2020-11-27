<template>
  <div id="chart">
    <apexchart type="scatter" height="350" width="800" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import Vue from 'vue'
import VueApexCharts from 'vue-apexcharts'

export default Vue.extend({
  name: 'AlertChart',
  components: {
    apexchart: VueApexCharts
  },
  data: function () {
    return {
      chartOptions: {
        chart: {
          height: 350,
          type: 'scatter',
          zoom: {
            type: 'xy'
          }
        },
        dataLabels: {
          enabled: false
        },
        grid: {
          xaxis: {
            lines: {
              show: true
            }
          },
          yaxis: {
            lines: {
              show: false
            }
          }
        },
        xaxis: {
          type: 'datetime',
          labels: {
            show: true
          }
        },
        yaxis: {
          max: 8,
          labels: {
            show: false
          }
        },
        colors: ['#7cfc00', '#ffff00', '#ff0000'],
        tooltip: {
          x: {
            show: false,
            format: 'HH:mm',
            formatter: undefined
          }
        }
      }
    }
  },
  computed: {
    series: function () {
      return [{
        name: '正常動作',
        data: this.$parent.time_normal
      }, {
        name: '注意',
        data: this.$parent.time_warning
      }, {
        name: 'アラート',
        data: this.$parent.time_alert
      }]
    }
  }
})
</script>
