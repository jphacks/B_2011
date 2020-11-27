<template>
  <div id="chart">
    <v-row>
      <v-col>
          <p style="font-size: 8pt; margin: 48px 9px 9px 9px; padding: 5px">トラフィック</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">SSHプロセス</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">音声</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">視線検出</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">顔認証</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">クリップボード</p>
          <p style="font-size: 8pt; margin: 9px; padding: 5px">ウィンドウ</p>
      </v-col>
      <v-col>
        <apexchart type="scatter" height="350" width="700" :options="chartOptions" :series="series"></apexchart>
      </v-col>
    </v-row>
  </div>
</template>
<style>
  /*.index {*/
  /*  font-size: 8pt;*/
  /*  margin: 6px;*/
  /*  padding: 5px;*/
  /*}*/
</style>
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
              show: true
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
