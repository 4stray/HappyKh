import { shallowMount } from '@vue/test-utils';
import ProfileComponent from '../../src/components/ProfileComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('ProfileComonent', () => {
  const wrapper = shallowMount(ProfileComponent);

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

  it('has male gender initially', () => {
    expect(ProfileComponent.data().userGender).to.be.equal('Male');
  });

});
