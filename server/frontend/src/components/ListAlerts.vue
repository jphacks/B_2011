<template>
  <div>
    <v-list-item three-line v-for="item in alerts" :key="item.message_id">
      <v-list-item-content>
        <v-card
          class="mx-auto"
          tile
          :to="{ name: 'examinee_report', params: { examinee_id: item.examinee_id }}"
        >
          <v-alert type='error' v-if='item.alert-1'>
            <v-list-item-title>
              受験者: {{item.examinee_id}}
            </v-list-item-title>
            <v-list-item-title>
              内容: {{item.module_name}}
            </v-list-item-title>
            <v-list-item-subtitle>
              詳細{{item.description}}
            </v-list-item-subtitle>

          </v-alert>
          <v-alert type='warning' v-else>
            <v-list-item-title>
              受験者: {{item.examinee_id}}
            </v-list-item-title>
            <v-list-item-title>
              内容: {{item.module_name}}
            </v-list-item-title>
            <v-list-item-subtitle>
              詳細{{item.description}}
            </v-list-item-subtitle>
          </v-alert>
        </v-card>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>
<script>
import Vue from 'vue'
import moment from 'moment'

export default Vue.extend({
  name: 'ListAlerts',
  computed: {
    alerts: function () {
      return this.$parent.alerts
    }
  },
  filters: {
    moment: function (date) {
      return moment(Date.parse(date)).format('HH:mm')
    }
  }
})
</script>
