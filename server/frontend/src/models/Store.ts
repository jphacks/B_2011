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
  getters: {
    exam_id: state => {
      return state.property.exam_id
    },
    examinee_id: state => {
      return state.property.examinee_id
    },
    alert_data: state => {
      return state.property.alert_data
    },
    exam_list: state => {
      return state.property.exam_list
    },
    status: state => {
      return state.property.status
    }
  },
  mutations: {
    setAlerts (state, response) {
      state.property.alert_data = JSON.parse(response).alert_data
      state.property.status = StatusConfig.LOADED
    },
    setExams (state, response) {
      console.log(JSON.parse(response))
      state.property.exam_list = JSON.parse(response).data
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
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/list?exam_id=' + this.state.property.exam_id, {
        mode: 'cors'
      }).then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
            commit('setAlerts', res)
          }
        )

    },
    getExamineeAlerts ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/list?examinee_id=' + this.state.property.examinee_id, {
        mode: 'cors'
      }).then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
            commit('setAlerts', res)
          }
        )
    },
    getExamList ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/exam/list', {
        mode: 'cors'
      }).then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
          commit('setExams', res)
          }
        )
    }
  }
})

export default PropertyStore
