import { shallowMount } from '@vue/test-utils';
import Cookies from 'js-cookie';
import Header
  from '../../src/components/Header.vue';
import { mapGetters } from 'vuex';

const expect = require('chai').expect;
const should = require('chai').should();

Cookies.set('token', 'value_');
Cookies.set('user_id', 'value_');

// describe('Header for authenticated user', () => {
//   const wrapper = shallowMount(Header, {
//     mocks: {
//       $cookies: Cookies,
//     },
//   });

  // it('has home button', () => {
  //   expect(wrapper.find('v-btn').text()).to.be.equal('Home');
  //   expect(wrapper.find('v-btn').attributes('to')).to.be.equal({name: 'home'});
  // });
  //
  // it('has profile button', () => {
  //   expect(wrapper.find('v-btn').text()).to.be.equal('Profile');
  // });
  //
  // it('has sign out button', () => {
  //   expect(wrapper.find('v-btn').text()).to.be.equal('Sign out');
  // });
});
