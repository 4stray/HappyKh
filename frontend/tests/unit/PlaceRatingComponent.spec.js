import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import Cookies from 'js-cookie';
import VueRouter from 'vue-router';
import PlaceRatingComponent from '../../src/components/PlaceRatingComponent.vue';

const localVue = createLocalVue();
localVue.use(VueRouter);
localVue.use(Vuetify);

const router = new VueRouter();
const expect = require('chai').expect;

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');
describe('PlaceRatingComponent', () => {
  const wrapper = shallowMount(PlaceRatingComponent, {
    localVue,
    router,
    mocks: {
      $cookies: Cookies,
    },
    methods: {
      fetchRating: () => {},
    },
  });
  it('has attribute for Rating', () => {
    expect(PlaceRatingComponent.data()).to.have.property('rating');
  });
  it('has label for Rating', () => {
    expect(wrapper.find('#labelRating').text()).to.be.equal('Rate this place:');
  });
  it('has button for rating places', () => {
    expect(wrapper.contains('[id="rating-btn"]')).to.be.equal(true);
  });
});
