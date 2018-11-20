import Vuetify from 'vuetify';
import { shallowMount, config, createLocalVue } from '@vue/test-utils';
import PlacesComponent from '@/components/PlacesComponent.vue';


const localVue = createLocalVue();
const expect = require('chai').expect;
const should = require('chai').should();

localVue.use(Vuetify);

config.mocks.$store = {
  state: {
    Authenticated: 'test token value',
  },
  getters: {
    getToken: state => state.Authenticated,
  },
};

describe('PlacesComponent', () => {
  const wrapper = shallowMount(PlacesComponent, { localVue });

  describe('has container for create place button and filter', () =>{
    it('itself', () => {
      expect(wrapper.contains('[name="menu-container"]')).to.be.equal(true);
    });

    const menu = wrapper.find('[name="menu-container"]');

    it('that contains add place button', () => {
       expect(menu.contains('[name="create-place-button"]')).to.be.equal(true);
    });

    it('that contains filter field', () => {
       expect(menu.contains('[name="filter"]')).to.be.equal(true);
    });

    it('that contains order select', () => {
       expect(menu.contains('[name="order-select"]')).to.be.equal(true);
    });
  });


  it('has container for place components', () => {
    expect(wrapper.contains('[name="place-container"]'))
      .to.be.equal(true);
  });
});
