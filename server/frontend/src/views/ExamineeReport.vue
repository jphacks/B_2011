<template>
  <div>
    <h1>受験者 {{ examinee_id }} についてのアラート</h1>
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
          <ListAlerts
            v-show="!is_loading"
            :alerts="alerts"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import Vue from 'vue'
import ListExaminees from '@/components/ListExaminees.vue'
import ListAlerts from '@/components/ListAlerts.vue'
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Examinee Report',
  components: {
    ListExaminees,
    ListAlerts
  },
  created: function () {
    this.$disconnect()
    const examinee_id = this.$route.params.examinee_id || 0
    this.$store.commit('setExamineeId', examinee_id)
    this.$store.dispatch('getExamineeAlerts')
  },
  watch: {
    $route () {
      const examinee_id = this.$route.params.examinee_id || 0
      this.$store.commit('setExamineeId', examinee_id)
      this.$store.dispatch('getExamineeAlerts')
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
    }
  }
})
</script>
