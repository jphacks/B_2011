<template>
  <div>
    <h1>{{ exam_name }}</h1>
    <div v-show="is_loading">
      Loading...
    </div>
    <v-container ma-0 pa-0>
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
            <ListAlerts
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
import ListAlerts from '@/components/ListAlerts.vue'
import ListExaminees from '@/components/ListExaminees.vue'
import AlertChart from '@/components/AlertChart.vue'
import StatusConfig from '@/config/Status.ts'
import Store from '../models/Store'

export default Vue.extend({
  name: 'Exam Report',
  created: function () {
    const exam_id = this.$route.params.exam_id || ''
    this.$store.commit('setExamId', exam_id)
    this.$store.dispatch('getExamInfo')
    this.$store.dispatch('getExamineeList')
    // modified for ws
    this.$disconnect()
    this.$store.state.property.alert_list = Array()
    this.$connect('ws://ben.hongo.wide.ad.jp:8000/ws/user/' + this.$route.params.exam_id || '', { store: Store, format: 'json' })
    // this.$store.dispatch('getExamAlerts')
  },
  components: {
    ListExaminees,
    ListAlerts,
    AlertChart
  },
  computed: {
    exam_name: function () {
      return this.$store.state.property.exam_name
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
