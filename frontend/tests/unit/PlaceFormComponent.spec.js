import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import PlaceFormComponent from '@/components/PlaceFormComponent.vue';


const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('PlaceFormComponent props', () => {
  const wrapper = shallowMount(PlaceFormComponent, { localVue });
  it('has place', () => {
    expect(wrapper.props('place')).to.be.an('Object');
  });

  describe('place fields', () => {
    it('has default place name field', () => {
      expect(wrapper.props('place')).has.property('name');
    });

    it('has default place description', () => {
      expect(wrapper.props('place')).has.property('description');
    });

    it('has default place logo', () => {
      expect(wrapper.props('place')).has.property('logo');
    });

    describe('place address fields', () => {
      it('has default place address', () => {
        expect(wrapper.props('place')).has.property('address')
          .to.be.an('Object');
      });
    });
  });
});

describe('mounted PlaceFormComponent', () => {
  const wrapper = shallowMount(PlaceFormComponent, { localVue });

  it('has place name field with "text" type', () => {
    expect(wrapper.find('#name').attributes('type'))
      .to.be.equal('text');
  });

  it('has place description textarea', () => {
    expect(wrapper.contains('#description')).to.be.equal(true);
  });

  it('contains default logo initially', () => {
    expect(wrapper.find('#logoImg').attributes('src'))
      .to.be.equal('/img/default_place.f065b10c.png');
  });

  it('has address autocomplete component', () => {
    expect(wrapper.contains('#placeAddress')).to.be.equal(true);
  });

  it('has logo input field with "file" type', () => {
    expect(wrapper.find('#logoInput').attributes('type')).to.be.equal('file');
  });

  it('check save button text', () => {
    expect(wrapper.find('[type=submit]').text()).to.be.equal('Save');
  });

  it('contains logo with equal src to data()', () => {
    wrapper.setData({
      place: {
        logo: 'testImage.png',
      },
    });

    expect(wrapper.find('#logoImg').attributes('src'))
      .to.be.equal(wrapper.vm.place.logo);
  });
});
