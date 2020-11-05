<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item v-repeat="exams">
      <v-list-item-content>
        <v-list-item-title>
          <router-link to='/exams/{{exam_id}}'>
            {{exam_id}}
          </router-link>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>
<script>
import Vue from 'vue'
import Store from '../models/Store.ts'

export default Vue.extend({
  name: 'ListExams',
  data: function () {
    return {
      exams: Store.state.property.exam_list
    }
  }
})
</script>
