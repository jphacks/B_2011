<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item v-repeat="alerts">
      <v-list-item-content>
        <router-link :to="{ name: 'examinee_report', params: { examinee_id: examinee_id }}">
          <v-alert type='error'>
            {{examinee_id}}
            {{module_name}}
            {{alert}}
            {{description}}
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
