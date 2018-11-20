import { shallowMount, createLocalVue } from '@vue/test-utils';
import Cookies from 'js-cookie';
import Vuetify from 'vuetify';
import ChangeEmailComponent
  from '../../src/components/ChangeEmailComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ChangeEmailComponent', () => {
  const wrapper = shallowMount(ChangeEmailComponent, {
    localVue,
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has field for new email', () => {
    expect(wrapper.find('#emailInput').exists()).to.be.equal(true);
  });

  it('has change submit button', () => {
    expect(wrapper.find('[type="submit"]').exists()).to.be.equal(true);
  });
});
