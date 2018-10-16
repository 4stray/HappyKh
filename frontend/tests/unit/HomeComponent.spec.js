import { shallowMount, mount, config, RouterLinkStub } from '@vue/test-utils';
import HomeComponent from '@/components/HomeComponent.vue';
import PlacesComponent from '@/components/PlacesComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

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
  const wrapper = mount(HomeComponent, config);
  it('has property msg', () => {
    expect(HomeComponent.props).to.have.key('msg');
  });

  it('has PlacesComponent', () => {
    expect(wrapper.contains(PlacesComponent)).to.be.equal(true);
  });
});
