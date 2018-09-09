import HomeComponent from '../../src/components/HomeComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('HomeComponent', () => {
  it('has property msg', () => {
    expect(HomeComponent.props).to.have.key('msg');
  });
});
