import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import confirmationEmail from '../../src/components/ConfirmationEmailComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('confirmationEmail', () => {
  const wrapper = shallowMount(confirmationEmail, { localVue });

  it('has default userEmail', () => {
    expect(confirmationEmail.data()).to.have.property('userEmail');
  });

  it('contains userEmail input field', () => {
    expect(wrapper.contains('[name="userEmail"]')).to.be.equal(true);
  });

  it('contains button for submitting user email', () => {
    expect(wrapper.contains('[class="btn-submit"]')).to.be.equal(true);
  });
});
