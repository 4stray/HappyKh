import Cookies from 'js-cookie';
import VueRouter from 'vue-router';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import PlaceDetail from '../../src/components/PlaceDetailComponent.vue';

const localVue = createLocalVue();
localVue.use(VueRouter);
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
    mocks: {
      $cookies: Cookies,
    },
  });
  wrapper.setData({
    placeLogo: '',
    placeName: '',
    placeDescription: '',
  });

  it('has default placeLogo', () => {
    expect(wrapper.find('#no_logo').attributes('src')).to.be.equal('/img/default_user.ce567c5b.png');
  });
  it('has default placeDescription', () => {
    expect(wrapper.find('#no_description').text()).to.be.equal('Place don\'t have a description.');
  });
});

describe('PlaceDetail for place with data', () => {
  const wrapper = shallowMount(PlaceDetail, {
    localVue,
    router,
    mocks: {
      $cookies: Cookies,
    },
  });
  const testUserData = {
    placeLogo: 'logo.png',
    placeName: 'name',
    placeDescription: 'description',
  };
  wrapper.setData(testUserData);

  it('has placeLogo', () => {
    expect(wrapper.find('img').attributes('src')).to.be.equal(testUserData.placeLogo);
  });

  it('has placeName', () => {
    expect(wrapper.find('#labelName').text()).to.be.equal('Name');
    expect(wrapper.find('#placeName').text()).to.be.equal(testUserData.placeName);
  });

  it('has placeDescription', () => {
    expect(wrapper.find('#labelDescription').text()).to.be.equal('Description');
    expect(wrapper.find('#placeDescription').text()).to.be.equal(testUserData.placeDescription);
  });
});
