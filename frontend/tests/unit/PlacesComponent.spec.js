import { shallowMount, config, RouterLinkStub, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import PlacesComponent from '../../src/components/PlacesComponent.vue';


const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

config.stubs['router-link'] = RouterLinkStub;
config.mocks.$awn = { alert: () => {} };
config.mocks.$store = {
  state: {
    Authenticated: 'test token value',
  },
  getters: {
    getToken: state => state.Authenticated,
  },
};
config.methods.getAllPlaces = () => {};

describe('PlacesComponent', () => {
  const wrapper = shallowMount(PlacesComponent, { localVue, config });

  it('has container for create place button and filter', () => {
    expect(wrapper.contains('[name="menu-container"]')).to.be.equal(true);
  });

  it('has button for adding place', () => {
    expect(wrapper.contains('[name="create-place-button"]')).to.be.equal(true);
  });

  it('has container for place components', () => {
    expect(wrapper.contains('[name="place-container"]'))
      .to.be.equal(true);
  });
});
