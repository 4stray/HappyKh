import Cookies from 'js-cookie';
import { shallowMount, config } from '@vue/test-utils';
import PlacesComponent from '../../src/components/PlacesComponent.vue';


const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', ' ');

describe('PlacesComponent', () => {
  const wrapper = shallowMount(PlacesComponent, {
    mocks: {
      $cookies: Cookies,
    }
  });

  it('has place holder', () => {
    expect(wrapper.contains('[class="place-holder"]')).to.be.equal(true);
  });

});
