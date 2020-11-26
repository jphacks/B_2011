<template>
  <v-card
    class="mx-auto"
    tile
  >
    <v-list-item three-line v-for="item in exams" :key="item.exam_id">
      <v-list-item-content>
        <router-link :to="{ name: 'exam_report', params: { exam_id: item.exam_id }}">
            <v-list-item-title>
              {{item.exam_name}}
            </v-list-item-title>
        </router-link>
        <v-list-item-subtitle>
          開催日: {{item.exam_date}}
        </v-list-item-subtitle>
        <v-list-item-subtitle>
          開始時刻: {{item.start_at}}
        </v-list-item-subtitle>
        <v-list-item-subtitle>
          終了時刻: {{item.end_at}}
        </v-list-item-subtitle>
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
