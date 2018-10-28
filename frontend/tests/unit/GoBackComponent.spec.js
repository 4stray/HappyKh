import { shallowMount } from '@vue/test-utils';
import GoBackComponent from '@/components/GoBackComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('GoBackComponent', () => {
  const wrapper = shallowMount(GoBackComponent);

  it('has button', () => {
    expect(wrapper.contains('v-btn')).to.be.equal(true);
  });

  describe('Go Back Button', () => {
    it('has icon in it', () => {
      expect(wrapper.find('v-btn').find('v-icon')
        .text()).to.be.equal('arrow_back');
    });
  })
});
