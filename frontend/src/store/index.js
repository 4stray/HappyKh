import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const state = {
    Authenticated: false,
    User: {

    },
};

const getters = {
    getAuthenticated: state => {
        return state.Authenticated;
    },
};
const actions = {

};

const mutations = {
    setAuthenticated(state, isAuthenticated) {
        state.Authenticated = isAuthenticated;
    },

};


export default new Vuex.Store({
    getters,
    actions,
    mutations,
    state
})