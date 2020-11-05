<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <div v-show="is_loading">
      Loading...
    </div>
    <ListExams v-show="!is_loading"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ListExams from '@/components/ListExams.vue' // @ is an alias to /src
import Store from '@/models/Store.ts'
import StatusConfig from '@/config/Status.ts'

export default Vue.extend({
  name: 'Home',
  computed: {
    is_loading: function () {
      return Store.state.property.status === StatusConfig.INITIALIZE
    }
  }
})

Store.dispatch('getExamList')
Vue.component('ListExams', ListExams)
</script>
