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
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Examinee Report',
  components: {
    ListAlerts
  },
  created: function () {
    const examinee_id = this.$route.params.examinee_id || 0
    this.$store.commit('setExamineeId', examinee_id)
    this.$store.dispatch('getExamineeAlerts')
  },
  computed: {
    is_loading: function () {
      return this.$store.getters.status === StatusConfig.INITIALIZE
    },
    alerts: function () {
      return this.$store.getters.property.alert_data
    }
  }
})
</script>
