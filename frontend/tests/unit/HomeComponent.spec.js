import { config, RouterLinkStub, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import HomeComponent from '@/components/HomeComponent.vue';


const localVue = createLocalVue();
localVue.use(Vuetify);

const expect = require('chai').expect;

config.stubs['router-link'] = RouterLinkStub;
config.stubs.PlacesComponent = '<div/>';
config.mocks.$store = {
  state: {
    Authenticated: 'test token',
  },
  getters: {
    getAuthenticated: state => !!state.Authenticated,
  },
};

describe('HomeComponent', () => {
  it('has property msg', () => {
    expect(HomeComponent.props).to.have.key('msg');
  });
});
