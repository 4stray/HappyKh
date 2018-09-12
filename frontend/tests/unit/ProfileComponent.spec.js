import { shallowMount } from '@vue/test-utils';
import ProfileComponent from '../../src/components/ProfileComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('ProfileComponent data() attributes check', () => {
  it('has userFirstName', () => {
    expect(ProfileComponent.data()).to.have.property('userFirstName');
  });

  it('has userLastName', () => {
    expect(ProfileComponent.data()).to.have.property('userLastName');
  });

  it('has userAge', () => {
    expect(ProfileComponent.data()).to.have.property('userAge');
  });

  it('has userEmail', () => {
    expect(ProfileComponent.data()).to.have.property('userEmail');
  });

  it('image change disabled initially', () => {
    expect(ProfileComponent.data().isDisabled).to.be.equal(true);
  });

  it('has button to enable edit suited text initially', () => {
    expect(ProfileComponent.data().enableText).to.be.equal('Enable editing');
  });

  it('has userGender', () => {
    expect(ProfileComponent.data()).to.have.property('userGender');
  });

  it('has userImage', () => {
    expect(ProfileComponent.data()).to.have.property('userImage');
  });
});

describe('ProfileComponent mounted check on fields', () => {
  const wrapper = shallowMount(ProfileComponent);

  it('contains LastName field', () => {
    expect(wrapper.contains('#last_name')).to.be.equal(true);
  });

  it('contains FirstName field', () => {
    expect(wrapper.contains('#first_name')).to.be.equal(true);
  });

  it('contains Age field', () => {
    expect(wrapper.contains('#age')).to.be.equal(true);
  });

  it('contains Email field', () => {
    expect(wrapper.contains('#email')).to.be.equal(true);
  });

  it('contains Image field', () => {
    expect(wrapper.contains('#image')).to.be.equal(true);
  })
});