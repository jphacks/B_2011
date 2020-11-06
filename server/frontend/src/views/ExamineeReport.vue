<template>
  <div>
    <div v-show="is_loading">
      Loading...
    </div>
    <ListAlerts
      v-show="!is_loading"
      :alerts="alerts" />
  </div>
</template>
<script>
import Vue from 'vue'
import ListAlerts from '@/components/ListAlerts.vue'
import Store from '@/models/Store.ts'
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Examinee Report',
  data: function () {
    return {
      alerts: Store.state.property.alert_data
    }
  },
  computed: {
    is_loading: function () {
      return Store.state.property.status === StatusConfig.INITIALIZE
    }
  }
})

const examinee_id = this.$route.params.examinee_id || 0
Store.commit('setExamineeId', examinee_id)
Store.dispatch('getExamineeAlerts')

Vue.component('ListAlerts', ListAlerts)

</script>
