import { shallowMount } from '@vue/test-utils';
import ProfileComponent from '../../src/components/ProfileComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('ProfileComponent data() check', () => {
  it('has userFirstName', () => {
    expect(ProfileComponent.data()).to.have.property('userFirstName');
  });

  it('has default userLastName', () => {
    expect(ProfileComponent.data()).to.have.property('userLastName');
  });

  it('has default userAge', () => {
    expect(ProfileComponent.data()).to.have.property('userAge');
  });

  it('has default userEmail', () => {
    expect(ProfileComponent.data()).to.have.property('userEmail');
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

describe('ProfileComponent after mounted check fields', () => {
  const wrapper = shallowMount(ProfileComponent);

  it('has LastName field with "text" type', () => {
    expect(wrapper.find('#last_name').attributes('type')).to.be.equal('text');
  });

  it('has FirstName field with "text" type', () => {
    expect(wrapper.find('#first_name').attributes('type')).to.be.equal('text');
  });

  it('has Age field with "number" type', () => {
    expect(wrapper.find('#age').attributes('type')).to.be.equal('number');
  });

  it('has Email field with "text" type', () => {
    expect(wrapper.find('#email').attributes('type')).to.be.equal('text');
  });

  it('contains Image from data()', () => {
    expect(wrapper.find('#image').attributes('src')).to.be.equal(ProfileComponent.data().userImage);
  });
});

describe('ProfileComponent interactions', () => {
  const wrapper = shallowMount(ProfileComponent);
  const btn = wrapper.find('.btn-change');
  btn.trigger('click');

  it('has interaction to enable fields on edit', () => {
    const email = wrapper.find('#email');
    expect(email.attributes('disabled')).to.be.equal(undefined);
  });

  it('has interaction to change buttons text', () => {
    expect(btn.text()).to.be.equal('Disable editing');
  });
});

describe('Django Server /profile', () => {
  it('has 401 error in response to unauthorized request', () => {
    const request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/api/users/profile/1', false);

    request.send();

    expect(request.status).to.be.equal(401);
  });

  it('has 200 status response to authorized user using token', () => {
    const request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8000/api/users/profile/5', false);

    request.setRequestHeader("Authorization", 'Token 1a0ccc1ff0455016164ddac9366af9c7711fe9ef');

    request.send();

    expect(request.status).to.be.equal(200);
  });
});
