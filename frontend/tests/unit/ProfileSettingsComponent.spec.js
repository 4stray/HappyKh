import Cookies from 'js-cookie';

import { shallowMount } from '@vue/test-utils';
import ProfileSettings from '../../src/views/ProfileSettings.vue';
import ProfileEditComponent
  from '../../src/components/ProfileEditComponent.vue';
import PasswordComponent from '../../src/components/PasswordComponent.vue';
import ChangeEmailComponent
  from '../../src/components/ChangeEmailComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ProfileSettingsComponent check', () => {
  const wrapper = shallowMount(ProfileSettings, {
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has 3 panels for change', () => {
    expect(wrapper.findAll('v-list-tile').length).to.be.equal(3);
  });

  it('has 1 change profile data component', () => {
    expect(wrapper.contains(ProfileEditComponent)).to.be.equal(true);
  });

  it('has 1 change password component', () => {
    expect(wrapper.contains(PasswordComponent)).to.be.equal(true);
  });

  it('has 1 change email component', () => {
    expect(wrapper.contains(ChangeEmailComponent)).to.be.equal(true);
  });
});
