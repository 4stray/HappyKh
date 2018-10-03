import { shallowMount, config } from '@vue/test-utils';
import PlacesComponent from '@/components/PlacesComponent.vue';


const expect = require('chai').expect;
const should = require('chai').should();

config.mocks['$store'] = {
  state: {
    Authenticated: 'test token value'
  },
  getters: {
    getToken: state => state.Authenticated,
  },
};

describe('PlacesComponent', () => {
  const wrapper = shallowMount(PlacesComponent, config);

  it('has places container', () => {
    expect(wrapper.contains('[class="places-container"]')).to.be.equal(true);
  });

  it('has button for adding place', () => {
    expect(wrapper.contains('[class="add-place-button"]')).to.be.equal(true);
  });

  it('has container for place components', () => {
    expect(wrapper.contains('[class="place-components-container"]'))
      .to.be.equal(true);
  });
});
