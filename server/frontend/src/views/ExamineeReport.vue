import AlertChart from "*.vue"
<template>
  <div>
    <h1>受験者 {{ examinee_id }} についてのアラート</h1>
    <div v-show="is_loading">
      Loading...
    </div>
    <v-container ma-5 pa-5>
      <v-row>
        <v-col cols="3">
          <ListExaminees
            v-show="!is_loading"
            :examinees="examinees"/>
        </v-col>
        <v-col cols="9">
          <v-row>
            <AlertChart
              :time_normal="time_normal"
              :time_warning="time_warning"
              :time_alert="time_alert"/>
          </v-row>
          <v-row>
            <ListAlertsExaminee
              v-show="!is_loading"
              :alerts="alerts"/>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import Vue from 'vue'
import ListExaminees from '@/components/ListExaminees.vue'
import ListAlertsExaminee from '@/components/ListAlertsExaminee.vue'
import AlertChart from '@/components/AlertChart.vue'
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Examinee Report',
  components: {
    ListExaminees,
    ListAlertsExaminee,
    AlertChart
  },
  created: function () {
    this.$disconnect()
    const examinee_id = this.$route.params.examinee_id || 0
    this.$store.commit('setExamineeId', examinee_id)
    this.$store.dispatch('getExamineeAlerts')
    this.$store.dispatch('getTimeListFromExaminee')
    this.$store.dispatch('getExamineeList')
  },
  watch: {
    $route () {
      const examinee_id = this.$route.params.examinee_id || 0
      this.$store.commit('setExamineeId', examinee_id)
      this.$store.dispatch('getExamineeAlerts')
      this.$store.dispatch('getTimeListFromExaminee')
      this.$store.dispatch('getExamineeList')
    }
  },
  computed: {
    examinee_id: function () {
      return this.$route.params.examinee_id
    },
    is_loading: function () {
      return this.$store.getters.status === StatusConfig.INITIALIZE
    },
    examinees: function () {
      return this.$store.getters.examinee_list
    },
    alerts: function () {
      return this.$store.getters.alert_list
    },
    time_normal: function () {
      return this.$store.getters.time_normal_list
    },
    time_warning: function () {
      return this.$store.getters.time_warning_list
    },
    time_alert: function () {
      return this.$store.getters.time_alert_list
    }
  }
})
</script>
