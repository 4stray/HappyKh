/* eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import {axiosInstance} from '../axios-config';

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
  getUserData: state => {
    return axiosInstance.get('/api/users/' + getters.getUserID(state));
  },
  getPlaces: state => {
    return axiosInstance.get('/api/places/');
  },
  getPlace: (state) => (id) => {
    return axiosInstance.get('/api/places/' + id);
  },
};

const actions = {
  signOut(state) {
    state.commit('signOut');
    axiosInstance.post('/api/users/logout')
      .then((response) => {
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
