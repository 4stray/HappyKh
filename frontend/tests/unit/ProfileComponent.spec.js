import Cookies from 'js-cookie';
import Profile from '../../src/views/Profile.vue';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('Profile data()', () => {
  it('has userFirstName', () => {
    expect(Profile.data()).to.have.property('userFirstName');
  });

  it('has default userLastName', () => {
    expect(Profile.data()).to.have.property('userLastName');
  });

  it('has default userAge', () => {
    expect(Profile.data()).to.have.property('userAge');
  });

  it('has default userGender', () => {
    expect(Profile.data()).to.have.property('userGender');
  });

  it('has default userImage', () => {
    expect(Profile.data()).to.have.property('userImage');
  });
});

