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
  });

  it('has 2 input fields', () => {
    expect(wrapper.findAll('v-text-field').length).to.be.equal(1);
    expect(wrapper.findAll('v-textarea').length).to.be.equal(1);
  });

  it('has placeName field with "text" type', () => {
    expect(wrapper.find('#name').attributes('type')).to.be.equal('text');
  });

  it('has logoInput field with "file" type', () => {
    expect(wrapper.find('#logoInput').attributes('type')).to.be.equal('file');
  });

  it('has placeDescription textarea', () => {
    expect(wrapper.contains('v-textarea')).to.be.equal(true);
  });

  it('contains default logo initially', () => {
    expect(wrapper.find('#default_logo').exists()).to.be.equal(true);
  });

  it('check save button text', () => {
    expect(wrapper.find('v-btn').text()).to.be.equal('Create Place');
  });

  it('contains logo with equal src to data()', () => {
    const newTestPlace = { placeLogo: 'imaginationImage.png' };
    wrapper.setData(newTestPlace);
    expect(wrapper.find('#logo').attributes('src')).to.be.equal(newTestPlace.placeLogo);
  });
});
