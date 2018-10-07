import { shallowMount } from '@vue/test-utils';
import Cookies from 'js-cookie';
import ChangeEmailComponent
  from '../../src/components/ChangeEmailComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ChangeEmailComponent', () => {
  const wrapper = shallowMount(ChangeEmailComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has field for new email', () => {
    expect(wrapper.find('v-text-field').exists()).to.be.equal(true);
  });

  it('has change submit button', () => {
    expect(wrapper.find('[type="submit"]').exists()).to.be.equal(true);
  });
});
