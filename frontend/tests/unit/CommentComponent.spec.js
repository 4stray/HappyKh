import Vuetify from 'vuetify';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import CommentComponent from '../../src/components/CommentComponent.vue';

const expect = require('chai').expect;

const localVue = createLocalVue();
localVue.use(Vuetify);

describe('CommentComponent', () => {
  const wrapper = shallowMount(CommentComponent, { localVue });

  it('contains avatar image', () => {
    expect(wrapper.contains('.avatar')).to.be.equal(true);
  });

  it('contains element with creation date', () => {
    expect(wrapper.contains('.creationDate')).to.be.equal(true);
  });

  it('contains element with author`s full name', () => {
    expect(wrapper.contains('.fullName')).to.be.equal(true);
  });

  it('contains control panel', () => {
    expect(wrapper.contains('.commentControl')).to.be.equal(false);
  });

  it('contains control commentUpdate button', () => {
    expect(wrapper.contains('.commentEdit')).to.be.equal(false);
  });

  it('contains control commentDelete button', () => {
    expect(wrapper.contains('.commentDelete')).to.be.equal(false);
  });
});
