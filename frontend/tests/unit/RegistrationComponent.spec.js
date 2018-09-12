import { shallowMount } from '@vue/test-utils';
import RegistrationComponent from '@/components/RegistrationComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('RegistrationComponent', () => {
  const wrapper = shallowMount(RegistrationComponent);

  it('is a vue instance', () => {
    expect(wrapper.isVueInstance()).to.be.equal(true)
  });
  
  it('has default userEmail', () => {
    expect(RegistrationComponent.data()).to.have.property('userEmail');
  });

  it('has default userPassword', () => {
    expect(RegistrationComponent.data()).to.have.property('userPassword');
  });

  it('contains username input field', () => {
    expect(wrapper.contains('[name="username"]')).to.be.equal(true);
  });
  it('contains password input field', () => {
    expect(wrapper.contains('[name="password"]')).to.be.equal(true);
  });

  it('contains confirmPassword input field', () => {
    expect(wrapper.contains('[name="confirmPassword"]')).to.be.equal(true);
  });

  it('contains button for submitting user credentials', () => {
    expect(wrapper.contains('[id="btn-registration"]')).to.be.equal(true);
  });
});