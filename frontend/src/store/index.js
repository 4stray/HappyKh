/* eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import {axiosInstance} from '../axios-requests';


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
  }
};

const actions = {
  signOut(state) {
    axiosInstance.post('/api/users/logout').then((response) => {
      console.log('Signed out');
    }).catch((error) => {
      console.log(error);
    }).finally(() => {
      state.commit('signOut');
    });
  },
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
