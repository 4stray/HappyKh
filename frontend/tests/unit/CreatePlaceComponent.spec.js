import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import CreatePlaceComponent from '@/components/CreatePlaceComponent.vue';


const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('mounted CreatePlaceComponent', () => {
  const wrapper = shallowMount(CreatePlaceComponent, { localVue });
  it('has card component', () => {
    expect(wrapper.contains('#createPlaceComponent')).to.be.equal(true);
  });
});
