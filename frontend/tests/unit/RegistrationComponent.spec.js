import { shallowMount, createLocalVue } from '@vue/test-utils';
import RegistrationComponent from '@/components/RegistrationComponent.vue';
import Vuetify from 'vuetify';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('RegistrationComponent check for vue instance', () => {
  const wrapper = shallowMount(RegistrationComponent, { localVue });

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
    expect(data).to.have.property('confirmationPassword', '');
  });
});


describe('RegistrationComponent contains the correct values', () => {
  const wrapper = shallowMount(RegistrationComponent, { localVue });


  it('is a vue instance', () => {
    expect(wrapper.isVueInstance()).to.be.equal(true);
  });

  it('contains userEmail input field', () => {
    expect(wrapper.contains('#userEmail')).to.be.equal(true);
  });

  it('contains userEmail placeholder suitable field attribute', () => {
    expect(wrapper.find('#userEmail').attributes('type')).to.be.equal('email');
  });

  it('contains userName input field', () => {
    expect(wrapper.contains('#userName')).to.be.equal(true);
  });

  it('contains userPassword input field', () => {
    expect(wrapper.contains('#userPassword')).to.be.equal(true);
  });

  it('contains userPassword placeholder suitable field attribute', () => {
    expect(wrapper.find('#userPassword').attributes('type'))
      .to.be.equal('password');
  });

  it('contains confirmationPassword input field', () => {
    expect(wrapper.contains('#confirmationPassword')).to.be.equal(true);
  });

  it('contains userPassword placeholder suitable field attribute', () => {
    expect(wrapper.find('#confirmationPassword').attributes('type'))
      .to.be.equal('password');
  });

  it('contains button for submitting user credentials', () => {
    expect(wrapper.contains('.btn-submit')).to.be.equal(true);
  });

  it('contains button with certain value', () => {
    expect(wrapper.find('.btn-submit').attributes())
      .property('value')
      .to.be.equal('REGISTER');
  });
});


describe('RegistrationComponent interactions', () => {
  const wrapper = shallowMount(RegistrationComponent, { localVue });
  const btn = wrapper.find('.btn-submit');

  it('button is not active if conditions are not met', () => {
    expect(btn.attributes()).property('disabled').to.be.equal('disabled');
  });
});
