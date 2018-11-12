import VueRouter from 'vue-router';
import {createLocalVue, shallowMount} from '@vue/test-utils';
import PlaceEditComponent from '@/components/PlaceEditComponent.vue';


const expect = require('chai').expect;
const localVue = createLocalVue();
const router = new VueRouter();

localVue.use(VueRouter);

describe('mounted PlaceEditComponent', () => {
  const wrapper = shallowMount(PlaceEditComponent, {
    localVue,
    router,
  });

  it('has card component', () => {
    expect(wrapper.contains('v-card#placeEditComponent')).to.be.equal(true);
  });
});
