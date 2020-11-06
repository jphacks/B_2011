import Vue from 'vue'
import Vuex from 'vuex'
import StatusConfig from '@/config/Status.ts'
Vue.use(Vuex)

const PropertyStore = new Vuex.Store({
  state: {
    property: {
      exam_id: '',
      examinee_id: '',
      alert_data: [],
      exam_list: [],
      status: StatusConfig.INITIALIZE
    }
  },
  mutations: {
    setAlerts (state, response) {
      // TODO: is the response valid form?
      state.property.alert_data = response.data.alert_data
      state.property.status = StatusConfig.LOADED
    },
    setExams (state, response) {
      // TODO: is the response valid form?
      state.property.exam_list = response.data.exam_list
      state.property.status = StatusConfig.LOADED
    },
    setExamId (state, id) {
      state.property.exam_id = id
    },
    setExamineeId (state, id) {
      state.property.examinee_id = id
    }
  },
  actions: {
    getExamAlerts ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/exams/' + this.state.property.exam_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            commit('setAlerts', res)
          }
        })
    },
    getExamineeAlerts ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/examinees/' + this.state.property.examinee_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            commit('setAlerts', res)
          }
        })
    },
    getExamList ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/exams', {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            commit('setExams', res)
          }
        })
    }
  }
})

export default PropertyStore
