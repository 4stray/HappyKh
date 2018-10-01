import { shallowMount } from '@vue/test-utils';
import PasswordComponent from '../../src/components/PasswordComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('Password data() check', () => {
    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('oldPassword');
    });

    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('newPassword');
    });

    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('confirmationPassword');
    });
});

describe('Password mounted fields check', () => {
    const wrapper = shallowMount(PasswordComponent);

    it('has 3 input fields', () => {
        expect(wrapper.findAll('input').length).to.be.equal(3);
    });

    it('has 3 fields with password type', () => {
        expect(wrapper.findAll('[type=password]').length).to.be.equal(3);
    });
});
