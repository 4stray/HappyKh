import Cookies from 'js-cookie';
import { shallowMount } from '@vue/test-utils';
import CreatePlaceComponent
  from '../../src/components/CreatePlaceComponent.vue';


const expect = require('chai').expect;

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('mounted CreatePlaceComponent', () => {
  const wrapper = shallowMount(CreatePlaceComponent);

  it('has card component', () => {
    expect(wrapper.contains('v-card#createPlaceComponent')).to.be.equal(true);
  });
});
