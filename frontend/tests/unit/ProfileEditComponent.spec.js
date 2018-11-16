import { shallowMount, createLocalVue } from '@vue/test-utils';
import Cookies from 'js-cookie';
import Vuetify from 'vuetify';
import ProfileEditComponent
  from '../../src/components/ProfileEditComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ProfileEditComponent', () => {
  const wrapper = shallowMount(ProfileEditComponent, {
    localVue,
    mocks: {
      $cookies: Cookies,
    },
    methods: {
      fetchFormData: () => {},
    },
  });

  it('has LastName field with "text" type', () => {
    expect(wrapper.find('#lastName').attributes('type')).to.be.equal('text');
  });

  it('has FirstName field with "text" type', () => {
    expect(wrapper.find('#firstName').attributes('type')).to.be.equal('text');
  });

  it('has Age field with "number" type', () => {
    expect(wrapper.find('#age').attributes('type')).to.be.equal('number');
  });

  it('has change Image button', () => {
    expect(wrapper.find('[type="file"]').exists()).to.be.equal(true);
  });

  it('has change submit button', () => {
    expect(wrapper.find('[type="submit"]').exists()).to.be.equal(true);
  });
});
