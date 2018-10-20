import { shallowMount } from '@vue/test-utils';
import PlaceComponent from '../../src/components/PlaceCollectionComponent.vue';


const expect = require('chai').expect;
const should = require('chai').should();

describe('PlaceComponent', () => {
  const wrapper = shallowMount(PlaceComponent);

  it('has attribute for place name', () => {
    expect(wrapper.contains('[class="place-name"]')).to.be.equal(true);
  });

  it('has property for place of a type object', () => {
    expect(PlaceComponent.props).to.have.key('place').to.be.an('object');
  });

  it('has attribute for place image', () => {
    expect(wrapper.contains('[class="place-image"]')).to.be.equal(true);
  });
});
