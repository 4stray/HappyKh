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

  it('contains userEmail input field', () => {
    expect(wrapper.contains('[type="email"]')).to.be.equal(true);
    expect(wrapper.contains('[placeholder="EMAIL"]')).to.be.equal(true);
  });

  it('contains password input field', () => {
    expect(wrapper.contains('[type="password"]')).to.be.equal(true);
    expect(wrapper.contains('[placeholder="PASSWORD"]')).to.be.equal(true);
  });

  it('contains confirmPassword input field', () => {
    expect(wrapper.contains('[type="password"]')).to.be.equal(true);
    expect(wrapper.contains('[placeholder="CONFIRM PASSWORD"]')).to.be.equal(true);
  });

  it('contains button for submitting user credentials', () => {
    expect(wrapper.contains('[class="btn-submit"]')).to.be.equal(true);
    expect(wrapper.contains('[type="submit"]')).to.be.equal(true);
    expect(wrapper.contains('[value="REGISTER"]')).to.be.equal(true);

  });
});
