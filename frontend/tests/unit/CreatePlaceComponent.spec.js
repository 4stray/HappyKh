import Cookies from 'js-cookie';
import { shallowMount } from '@vue/test-utils';
import createPlaceComponent from '../../src/components/CreatePlaceComponent.vue';


const expect = require('chai').expect;

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

describe('createPlaceComponent data()', () => {
  it('has placeName', () => {
    expect(createPlaceComponent.data()).to.have.property('placeName');
  });

  it('has default placeAddress', () => {
    expect(createPlaceComponent.data()).to.have.property('placeDescription');
  });

  it('has default placeDescription', () => {
    expect(createPlaceComponent.data()).to.have.property('placeDescription');
  });

  it('has default placeLogo', () => {
    expect(createPlaceComponent.data()).to.have.property('placeLogo');
  });
});

describe('mounted createPlaceComponent', () => {
  const wrapper = shallowMount(createPlaceComponent, {
    mocks: {
      $cookies: Cookies,
    },
    stubs: {
      places: '<div/>',
    },
  });

  it('has 2 input fields', () => {
    expect(wrapper.findAll('input').length).to.be.equal(3);
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

  it('has address autocomplete component', () => {
    expect(wrapper.contains('#placeAddress')).to.be.equal(true);
  });

  it('contains logo from data()', () => {
    expect(wrapper.find('#logo').attributes('src')).to.be.equal(createPlaceComponent.data().placeLogo);
  });

  it('check save button text', () => {
    expect(wrapper.find('.btn-save').text()).to.be.equal('Create Place');
  });

  it('button is not active if conditions are not met', () => {
    expect(wrapper.find('.btn-save').attributes()).property('disabled').to.be.equal('disabled');
  });
});
