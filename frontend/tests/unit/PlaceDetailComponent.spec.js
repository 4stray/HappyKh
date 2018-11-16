import Cookies from 'js-cookie';
import Vuex from 'vuex';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';
import PlaceDetail from '@/components/PlaceDetailComponent.vue';
import { shallowMount, createLocalVue } from '@vue/test-utils';

const localVue = createLocalVue();
const router = new VueRouter();
const expect = require('chai').expect;
const should = require('chai').should();

localVue.use(VueRouter);
localVue.use(Vuex);
localVue.use(Vuetify);

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');


describe('PlaceDetail data()', () => {
  it('has place property', () => {
    expect(PlaceDetail.data()).to.have.property('place');
    // expect(wrapper.props('place')).to.be.an('Object');
  });

  it('has default place name property', () => {
    expect(PlaceDetail.data()).to.have.property('place')
      .to.have.property('name');
  });

  it('has place', () => {
    expect(PlaceDetail.data()).to.have.property('place');
  });
});

describe('PlaceDetail for empty place', () => {
  const wrapper = shallowMount(PlaceDetail, {
    localVue,
    router,
  });
  wrapper.setData({
    place: {
      name: '',
      description: '',
      logo: '',
      address: {
        address: '',
        longitude: 0,
        latitude: 0,
      },
    },
  });

  it('has default place logo', () => {
    expect(wrapper.find('#logoImg').attributes('src'))
      .to.be.equal('/img/default_place.f065b10c.png');
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
    place: {
      logo: 'logo.png',
      name: 'name',
      description: 'description',
      address: {
        longitude: 50,
        latitude: 49,
        address: 'test addresss',
      },
    },
  };
  wrapper.setData(testUserData);

  it('has place logo', () => {
    expect(wrapper.find('#logoImg').attributes('src'))
      .to.be.equal(testUserData.place.logo);
  });

  it('has place name', () => {
    expect(wrapper.find('#placeName').text())
      .to.be.equal(testUserData.place.name);
  });

  it('has place description', () => {
    expect(wrapper.find('#placeDescription').text())
      .to.be.equal(testUserData.place.description);
  });

  it('has place address', () => {
    expect(wrapper.find('#labelAddress').text()).to.be.equal('Address');
    expect(wrapper.find('#placeAddress').text())
      .to.be.equal(testUserData.place.address.address);
  });
});
