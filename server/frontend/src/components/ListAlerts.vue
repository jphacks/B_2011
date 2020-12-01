<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item three-line v-for="item in alerts" :key="item.message_id">
      <v-list-item-content>
        <router-link :to="{ name: 'examinee_report', params: { examinee_id: item.examinee_id }}">
          <v-alert type='error' v-if='item.alert'>
            <v-list-item-title>
              アラートID: {{item.message_id}}
              時刻: {{item.created_at}}
            </v-list-item-title>
            <v-list-item-subtitle>
              受験者: {{item.examinee_id}}
              内容: {{item.module_name}}
            </v-list-item-subtitle>
            <v-list-item-subtitle>
              {{item.description}}
              {{item.content}}
            </v-list-item-subtitle>
          </v-alert>
          <v-alert type='warning' v-else>
            <v-list-item-title>
              アラートID: {{item.message_id}}
              時刻: {{item.created_at}}
            </v-list-item-title>
            <v-list-item-subtitle>
              受験者: {{item.examinee_id}}
              内容: {{item.module_name}}
            </v-list-item-subtitle>
            <v-list-item-subtitle>
              {{item.description}}
              {{item.content}}
            </v-list-item-subtitle>
          </v-alert>
        </router-link>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>
<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'ListAlerts',
  computed: {
    alerts: function () {
      console.log('alerts:', this.$parent.alerts)
      return this.$parent.alerts
    }
  }
})
</script>
