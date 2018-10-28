import { shallowMount, mount, config } from '@vue/test-utils';
import HomeComponent from '@/components/HomeComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

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
});
