import { shallowMount } from '@vue/test-utils';
import ProfileComponent from '../../src/components/ProfileComponent.vue';
import Cookies from 'js-cookie';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('ProfileComponent data()', () => {
  it('has userFirstName', () => {
    expect(ProfileComponent.data()).to.have.property('userFirstName');
  });

  it('has default userLastName', () => {
    expect(ProfileComponent.data()).to.have.property('userLastName');
  });

  it('has default userAge', () => {
    expect(ProfileComponent.data()).to.have.property('userAge');
  });

  it('fields edit disabled initially', () => {
    expect(ProfileComponent.data().isDisabled).to.be.equal(true);
  });

  it('has default enableText', () => {
    expect(ProfileComponent.data().enableText).to.be.equal('Enable editing');
  });

  it('has default userGender', () => {
    expect(ProfileComponent.data()).to.have.property('userGender');
  });

  it('has default userImage', () => {
    expect(ProfileComponent.data()).to.have.property('userImage');
  });
});

describe('mounted ProfileComponent', () => {
  const wrapper = shallowMount(ProfileComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has 4 input fields', () => {
    expect(wrapper.findAll('input').length).to.be.equal(4);
  });
  it('has 1 selection element', () => {
    expect(wrapper.findAll('select').length).to.be.equal(1);
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
    expect(wrapper.find('#image').attributes('src')).to.be.equal(ProfileComponent.data().userImage);
  });
});

describe('ProfileComponent interactions', () => {
  const wrapper = shallowMount(ProfileComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });
  const btn = wrapper.find('.btn-change');
  btn.trigger('click');

  it('has interaction to enable fields on edit', () => {
    const email = wrapper.find('#first_name');
    expect(email.attributes('disabled')).to.be.equal(undefined);
  });

  it('has interaction to change buttons text', () => {
    expect(btn.text()).to.be.equal('Disable editing');
  });
});
