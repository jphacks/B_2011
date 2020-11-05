<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item v-repeat="alerts">
      <v-list-item-content>
        <router-link to='/examinees/{{examinee_id}}'>
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
import Store from '../models/Store.ts'

export default Vue.extend({
  name: 'ListAlerts',
  data: function () {
    return {
      alerts: Store.state.property.alert_data
    }
  }
})
</script>
