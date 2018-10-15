import { shallowMount } from '@vue/test-utils';
import confirmationEmail from '../../src/components/ConfirmationEmailComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('confirmationEmail', () => {
  const wrapper = shallowMount(confirmationEmail);

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
