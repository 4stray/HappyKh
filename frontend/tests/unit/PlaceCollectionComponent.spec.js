import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import PlaceComponent from '../../src/components/PlaceCollectionComponent.vue';


const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);


describe('PlaceComponent', () => {
  const wrapper = shallowMount(PlaceComponent, { localVue });

  it('has attribute for place name', () => {
    expect(wrapper.contains('[name="place-name"]')).to.be.equal(true);
  });

  it('has property for place of a type object', () => {
    expect(PlaceComponent.props).to.have.key('place').to.be.an('object');
  });

  it('has attribute for place image', () => {
    expect(wrapper.contains('[name="place-image"]')).to.be.equal(true);
  });
});
