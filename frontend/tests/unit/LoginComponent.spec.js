import LoginComponent from '../../src/components/LoginComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('LoginComonent', () => {
  it('has default userEmail', () => {
    expect(LoginComponent.data()).to.have.property('userEmail');
  });

  it('has default userPassword', () => {
    expect(LoginComponent.data()).to.have.property('userPassword');
  });
});

describe('Django Server', () => {
  it('login API', () => {
    const request = new XMLHttpRequest();

    request.open('POST', 'http://localhost:8000/api/users/login/', false);

    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    request.send(JSON.stringify({ user_email: 'abc@gmail.com' }));

    expect(request.status).to.be.equal(200);
  });
});
