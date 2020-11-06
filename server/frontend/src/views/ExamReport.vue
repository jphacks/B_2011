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
  name: 'Exam Report',
  created: function () {
    const exam_id = this.$route.params.exam_id || ''
    this.$store.commit('setExamId', exam_id)
    this.$store.dispatch('getExamAlerts')
  },
  components: {
    ListAlerts
  },
  computed: {
    is_loading: function () {
      return this.$store.getters.status === StatusConfig.INITIALIZE
    },
    alerts: function () {
      return this.$store.getters.alert_data
    }
  }
})

</script>
