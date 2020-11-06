<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <div v-show="is_loading">
      Loading...
    </div>
    <ListExams
      v-show="!is_loading"
      :exam_list="exam_list"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ListExams from '@/components/ListExams.vue' // @ is an alias to /src
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Home',
  created: function () {
    this.$store.dispatch('getExamList')
  },
  components: {
    ListExams
  },
  computed: {
    is_loading: function () {
      return this.$store.getters.status === StatusConfig.INITIALIZE
    },
    exam_list: function () {
      return this.$store.getters.exam_list
    }
  }
})
</script>
