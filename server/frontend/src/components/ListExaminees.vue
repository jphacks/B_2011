<template>
  <div>
    <v-list-item three-line v-for="item in examinees" :key="item.examinee_id">
      <v-list-item-content>
        <v-card
          class="mx-auto"
          tile
          :to="{ name: 'examinee_report', params: { examinee_id: item.examinee_id }}"
        >
          <v-card-title>受験者ID</v-card-title>
          <v-card-text>{{item.examinee_id}}</v-card-text>
        </v-card>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>
<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'ListExaminees',
  computed: {
    examinees: function () {
      return this.$parent.examinees
    }
  }
})
</script>
