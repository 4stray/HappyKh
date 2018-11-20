import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import { createLocalVue, shallowMount } from '@vue/test-utils';
import PlaceEditComponent from '@/components/PlaceEditComponent.vue';


const expect = require('chai').expect;

const localVue = createLocalVue();
const router = new VueRouter();

localVue.use(Vuetify);
localVue.use(VueRouter);

describe('mounted PlaceEditComponent', () => {
  const wrapper = shallowMount(PlaceEditComponent, {
    localVue,
    router,
    mocks: {
      $awn: {
        alert: () => {},
      },
    },
    methods: {
      fetchPlaceEditingPermission: () => {},
      fetchPlaceData: () => {},
    },
  });

  it('has card component', () => {
    expect(wrapper.contains('#placeEditComponent')).to.be.equal(true);
  });
});
