import Cookies from 'js-cookie';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import PlaceDetail from '../../src/components/PlaceDetailComponent.vue';

const localVue = createLocalVue();
localVue.use(VueRouter);
localVue.use(Vuex);
const router = new VueRouter();
const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');


describe('PlaceDetail data()', () => {
  it('has placeLogo', () => {
    expect(PlaceDetail.data()).to.have.property('placeLogo');
  });

  it('has default placeName', () => {
    expect(PlaceDetail.data()).to.have.property('placeName');
  });

  it('has default placeDescription', () => {
    expect(PlaceDetail.data()).to.have.property('placeDescription');
  });
});

describe('PlaceDetail for empty place', () => {
  const wrapper = shallowMount(PlaceDetail, {
    localVue,
    router,
  });
  wrapper.setData({
    placeLogo: '',
    placeName: '',
    placeDescription: '',
    placeAddress: '',
  });

  it('has default placeLogo', () => {
    expect(wrapper.find('v-img').attributes('src')).to.be.equal('/img/default_place.f065b10c.png');
  });
  it('has default placeDescription', () => {
    expect(wrapper.find('#no_description').text()).to.be.equal('Place has no description.');
  });
});

describe('PlaceDetail for place with data', () => {
  const wrapper = shallowMount(PlaceDetail, {
    localVue,
    router,
  });
  const testUserData = {
    placeLogo: 'logo.png',
    placeName: 'name',
    placeDescription: 'description',
    placeAddress: 'some address',
  };
  wrapper.setData(testUserData);

  it('has placeLogo', () => {
    expect(wrapper.find('v-img').attributes('src')).to.be.equal(testUserData.placeLogo);
  });

  it('has placeName', () => {
    expect(wrapper.find('#placeName').text()).to.be.equal(testUserData.placeName);
  });

  it('has placeDescription', () => {
    expect(wrapper.find('#placeDescription').text()).to.be.equal(testUserData.placeDescription);
  });

  it('has placeAddress', () => {
    expect(wrapper.find('#labelAddress').text()).to.be.equal('Address');
    expect(wrapper.find('#placeAddress').text()).to.be.equal(testUserData.placeAddress);
  });
});
