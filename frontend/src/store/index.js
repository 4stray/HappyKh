/* eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);
const state = {
  Authenticated: window.$cookies.get('token'),
  UserID: window.$cookies.get('user_id'),
};

const getters = {
  getAuthenticated: state => {
    return !!getters.getToken(state);
  },
  getToken: state => {
    return state.Authenticated;
  },
  getUserID: state => {
    return state.UserID;
  },
};

const actions = {
  signOut(state) {
    const urlLogOut =
      'http://127.0.0.1:8000/api/users/logout';

    const token = this.getters.getToken;

    state.commit('signOut');

    axios.post(
      urlLogOut,
      {},
      {
        headers: { Authorization: `Token ${token}` },
      }).then((response) => {
        console.log('Signed out');
      }).catch((error) => {
        console.log(error);
      });
  }
};

const mutations = {
  signOut(state) {
    mutations.setAuthenticated(state, false);
    window.$cookies.remove('token');
    mutations.setUserID(state, null);
    window.$cookies.remove('user_id');
  },
  setAuthenticated(state, isAuthenticated) {
    state.Authenticated = isAuthenticated;
  },
  setUserID(state, UserID) {
    state.UserID = UserID;
  },
};

export default new Vuex.Store({
  getters,
  actions,
  mutations,
  state,
});
