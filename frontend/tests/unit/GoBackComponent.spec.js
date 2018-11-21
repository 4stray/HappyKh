import { createLocalVue, mount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import GoBackComponent from '@/components/GoBackComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('GoBackComponent', () => {
  const wrapper = mount(GoBackComponent, { localVue });

  it('has button', () => {
    expect(wrapper.contains('#goBackButton')).to.be.equal(true);
  });

  describe('Go Back Button', () => {
    it('has icon in it', () => {
      expect(wrapper.find('#goBackButton').find('#iconBack')
        .text()).to.be.equal('arrow_back');
    });
  });
});
