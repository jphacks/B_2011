<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item v-for="(exam, idx) in exams" :key="idx">
      <v-list-item-content>
        <v-list-item-title>
          <router-link :to="{ name: 'exam_report', params: { exam_id: exam }}">
            {{ exam }}
          </router-link>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>
<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'ListExams',
  computed: {
    exams: function () {
      return this.$parent.exam_list
    }
  }
})
</script>
