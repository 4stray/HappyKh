import { shallowMount } from '@vue/test-utils';
import CreatePlaceComponent from '@/components/CreatePlaceComponent.vue';


const expect = require('chai').expect;

describe('mounted CreatePlaceComponent', () => {
  const wrapper = shallowMount(CreatePlaceComponent);

  it('has card component', () => {
    expect(wrapper.contains('v-card#createPlaceComponent')).to.be.equal(true);
  });
});
