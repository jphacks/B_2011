import Vue from 'vue'
import Vuex from 'vuex'
import StatusConfig from '@/config/Status.ts'
Vue.use(Vuex)

const PropertyStore = new Vuex.Store({
  state: {
    property: {
      exam_id: '',
      exam_name: '',
      examinee_id: '',
      alert_list: Array(),
      exam_list: [],
      examinee_list : [],

      //チャート用のリスト
      time_normal_list: [],
      time_warning_list: [],
      time_alert_list: [],
      status: StatusConfig.INITIALIZE,
    },
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
    },
  },
  getters: {
    exam_id: state => {
      return state.property.exam_id
    },
    exam_name: state => {
      return state.property.exam_name
    },
    examinee_id: state => {
      return state.property.examinee_id
    },
    alert_list: state => {
      return state.property.alert_list
    },
    exam_list: state => {
      return state.property.exam_list
    },
    examinee_list: state => {
      return state.property.examinee_list
    },
    //チャート用リスト
    time_normal_list: state => {
      return state.property.time_normal_list
    },
    time_warning_list: state => {
      return state.property.time_warning_list
    },
    time_alert_list: state => {
      return state.property.time_alert_list
    },
    status: state => {
      return state.property.status
    },
  },
  mutations: {
    setExamInfo (state, response) {
      var data = JSON.parse(response).exam_data
      state.property.exam_name = data.exam_name
      state.property.status = StatusConfig.LOADED
    },
    setAlerts (state, response) {
      state.property.alert_list = JSON.parse(response).alert_data
      state.property.status = StatusConfig.LOADED
    },
    setExams (state, response) {
      state.property.exam_list = JSON.parse(response).exam_data
      state.property.status = StatusConfig.LOADED
    },
    setExaminees (state, response) {
      state.property.examinee_list = JSON.parse(response).examinee_data
      state.property.status = StatusConfig.LOADED
    },
    setTimeList (state, response) {
      const data = JSON.parse(response)

      state.property.time_normal_list = data.time_normal_list
      state.property.time_warning_list = data.time_warning_list
      state.property.time_alert_list = data.time_alert_list
      state.property.status = StatusConfig.LOADED
    },
    setExamId (state, id) {
      state.property.exam_id = id
    },
    setExamineeId (state, id) {
      state.property.examinee_id = id
    },
    // for websocket connection
    SOCKET_ONOPEN (state, event)  {
      Vue.prototype.$socket = event.currentTarget
      state.socket.isConnected = true
    },
    SOCKET_ONCLOSE (state, event)  {
      state.socket.isConnected = false
    },
    SOCKET_ONERROR (state, event)  {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
      state.socket.message = message
      state.property.alert_list.unshift(message)
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  },
  actions: {
    getExamInfo ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/exam/?exam_id=' + this.state.property.exam_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
        commit('setExamInfo', res)
      })
    },
    getExamAlerts ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/list?exam_id=' + this.state.property.exam_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
          commit('setAlerts', res)
        })
    },
    getExamineeAlerts ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/list?examinee_id=' + this.state.property.examinee_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
          commit('setAlerts', res)
        })
    },
    getExamList ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/exam/list', {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
          commit('setExams', res)
        })
    },
    getExamineeList ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/examinee/list?exam_id=' + this.state.property.exam_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
        commit('setExaminees', res)
      })
    },
    getTimeListFromExaminee ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/timelist?examinee_id=' + this.state.property.examinee_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
        commit('setTimeList', res)
      })
    },
    getTimeListFromExam ({ commit }) {
      fetch(process.env.VUE_APP_API_SERVER_URL + '/api/message/timelist?exam_id=' + this.state.property.exam_id, {
        mode: 'cors'
      })
        .then(res => {
          if (res.status === 200) {
            return res.json()
          }
        }).then(res => {
        commit('setTimeList', res)
      })
    }
  }
})

export default PropertyStore
