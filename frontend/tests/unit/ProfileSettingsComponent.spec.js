import Cookies from 'js-cookie';
import Vuetify from 'vuetify';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import ProfileSettings from '../../src/views/ProfileSettings.vue';
import ProfileEditComponent
  from '../../src/components/ProfileEditComponent.vue';
import PasswordComponent from '../../src/components/PasswordComponent.vue';
import ChangeEmailComponent
  from '../../src/components/ChangeEmailComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);
Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ProfileSettings check', () => {
  const wrapper = shallowMount(ProfileSettings, {
    localVue,
    mocks: {
      $cookies: Cookies,
    },
    methods: {
      fetchFormData: () => {},
    },
  });

  it('has 2 tabs for change', () => {
    expect(wrapper.findAll('.v-card').length).to.be.equal(2);
  });

  it('has ProfileEditComponent component', () => {
    expect(wrapper.contains(ProfileEditComponent)).to.be.equal(true);
  });
});

describe('ProfileSettings interactions', () => {
  const wrapper = shallowMount(ProfileSettings, {
    localVue,
    mocks: {
      $cookies: Cookies,
    },
    methods: {
      fetchFormData: () => {},
    },
  });
  const tabs = wrapper.findAll('.settingsTabs');
  it('has 1 component ProfileEditComponent after click on the first tab', () => {
    tabs.at(0).trigger('click');
    expect(wrapper.contains(ProfileEditComponent)).to.be.equal(true);
  });

  it('has 1 component PasswordComponent after click on the second tab', () => {
    tabs.at(1).trigger('click');
    expect(wrapper.contains(PasswordComponent)).to.be.equal(true);
  });

  it('has 1 component ChangeEmailComponent after click on the third tab', () => {
    tabs.at(2).trigger('click');
    expect(wrapper.contains(ChangeEmailComponent)).to.be.equal(true);
  });
});
