/* eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);
const state = {
  Authenticated: window.$cookies.get('token'),
};

const USER_ID = window.$cookies.get('user_id') || 'XG';

const getters = {
  getAuthenticated: state => {
    return !!getters.getToken(state);
  },
  getToken: state => {
    return state.Authenticated;
  },
  getUserData: state => {
    return axios.get('/api/users/' + USER_ID);
  }
};

const actions = {
  signOut(state) {
    const urlLogOut = '/api/users/logout';
    state.commit('signOut');
    axios.post(
      urlLogOut,
    ).then((response) => {
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
    window.$cookies.remove('user_id');
  },
  setAuthenticated(state, isAuthenticated) {
    state.Authenticated = isAuthenticated;
  },
};

export default new Vuex.Store({
  getters,
  actions,
  mutations,
  state,
});
