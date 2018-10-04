import Cookies from 'js-cookie';
import { shallowMount } from '@vue/test-utils';
import createPlaceComponent from '../../src/components/CreatePlaceComponent.vue';


const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('createPlaceComponent data()', () => {
  it('has placeName', () => {
    expect(createPlaceComponent.data()).to.have.property('placeName');
  });

  it('has default placeDescription', () => {
    expect(createPlaceComponent.data()).to.have.property('placeDescription');
  });

  it('has default placeLogo', () => {
    expect(createPlaceComponent.data()).to.have.property('placeLogo');
  });

  // it('has default user', () => {
  //  expect(createPlaceComponent.data()).to.have.property('user');
  // });
});

describe('mounted createPlaceComponent', () => {
  const wrapper = shallowMount(createPlaceComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });

  it('has 2 input fields', () => {
    expect(wrapper.findAll('input').length).to.be.equal(2);
  });
  it('has placeName field with "text" type', () => {
    expect(wrapper.find('#name').attributes('type')).to.be.equal('text');
  });

  it('has logoInput field with "file" type', () => {
    expect(wrapper.find('#logoInput').attributes('type')).to.be.equal('file');
  });

  it('has placeDescription textarea', () => {
    expect(wrapper.contains('textarea')).to.be.equal(true);
  });

  it('contains logo from data()', () => {
    expect(wrapper.find('#logo').attributes('src')).to.be.equal(createPlaceComponent.data().placeLogo);
  });
});

describe('createPlaceComponent interactions', () => {
  const wrapper = shallowMount(createPlaceComponent, {
    mocks: {
      $cookies: Cookies,
    },
  });
  const btn = wrapper.find('.btn-save');
  btn.trigger('click');

  it('has interaction to change buttons text', () => {
    expect(btn.text()).to.be.equal('Create Place');
  });
});
