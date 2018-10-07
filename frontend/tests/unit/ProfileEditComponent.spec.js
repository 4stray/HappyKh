import { shallowMount } from '@vue/test-utils';
import Cookies from 'js-cookie';
import ProfileEditComponent
  from '../../src/components/ProfileEditComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ProfileEditComponent', () => {
  const wrapper = shallowMount(ProfileEditComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has LastName field with "text" type', () => {
    expect(wrapper.find('#last_name').attributes('type')).to.be.equal('text');
  });

  it('has FirstName field with "text" type', () => {
    expect(wrapper.find('#first_name').attributes('type')).to.be.equal('text');
  });

  it('has Age field with "number" type', () => {
    expect(wrapper.find('#age').attributes('type')).to.be.equal('number');
  });

  it('contains Image from data()', () => {
    expect(wrapper.find('#image').attributes('src')).to.be.equal(ProfileEditComponent.data().userImage);
  });

  it('has change Image button', () => {
    expect(wrapper.find('[type="file"]').exists()).to.be.equal(true);
  });

  it('has change submit button', () => {
    expect(wrapper.find('[type="submit"]').exists()).to.be.equal(true);
  });
});
