import { shallowMount } from '@vue/test-utils';
import RegistrationComponent from '@/components/RegistrationComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();


describe('RegistrationComponent check for vue instance', () => {
  const wrapper = shallowMount(RegistrationComponent);

  it('is a vue instance', () => {
    expect(wrapper.isVueInstance()).to.be.equal(true);
  });
});


describe('RegistrationComponent data', () => {
  const data = RegistrationComponent.data();

  it('has default userEmail', () => {
    expect(data).to.have.property('userEmail', '');
  });

  it('has default userPassword', () => {
    expect(data).to.have.property('userPassword', '');
  });

  it('has default confirmPassword', () => {
    expect(data).to.have.property('confirmPassword', '');
  });

  it('has defalut errors', () => {
    expect(data).to.have.deep.property('errors', {
      email: '',
      password: [],
    });
  });
});


describe('RegistrationComponent contains the corrcet values', () => {
  const wrapper = shallowMount(RegistrationComponent);

  it('is a vue instance', () => {
    expect(wrapper.isVueInstance()).to.be.equal(true);
  });

  it('contains userEmail input field', () => {
    expect(wrapper
      .find('#userEmail')
      .attributes())
      .property('type')
      .to.be.equal('email');
  });

  it('contains userEmail placeholder suitable field attribute', () => {
    expect(wrapper
      .find('#userEmail')
      .attributes())
      .property('placeholder')
      .to.be.equal('EMAIL');
  });

  it('contains userPassword input field', () => {
    expect(wrapper
      .find('#userPassword')
      .attributes())
      .property('type')
      .to.be.equal('password');
  });

  it('contains userPassword placeholder suitable field attribute', () => {
    expect(wrapper
      .find('#userPassword')
      .attributes())
      .property('placeholder')
      .to.be.equal('PASSWORD');
  });

  it('contains userPassword input field', () => {
    expect(wrapper
      .find('#confirmPassword')
      .attributes())
      .property('type')
      .to.be.equal('password');
  });

  it('contains userPassword placeholder suitable field attribute', () => {
    expect(wrapper
      .find('#confirmPassword')
      .attributes())
      .property('placeholder')
      .to.be.equal('CONFIRM PASSWORD');
  });

  it('contains button for submitting user credentials', () => {
    expect(wrapper
      .find('.btn-submit')
      .attributes())
      .property('type')
      .to.be.equal('submit');
  });

  it('contains button with certain value', () => {
    expect(wrapper
      .find('.btn-submit')
      .attributes())
      .property('value')
      .to.be.equal('REGISTER');
  });
});


describe('RegistrationComponent interactions', () => {
  const wrapper = shallowMount(RegistrationComponent);
  const btn = wrapper.find('.btn-submit');

  it('button is not active if conditions are not met', () => {
    expect(btn.attributes()).property('disabled').to.be.equal('disabled');
  });
});
