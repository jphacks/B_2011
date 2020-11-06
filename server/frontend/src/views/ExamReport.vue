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
  name: 'Exam Report',
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

const exam_id = this.$route.params.exam_id || 0
Store.commit('setExamId', exam_id)
Store.dispatch('getExamAlerts')

Vue.component('ListAlerts', ListAlerts)

</script>
