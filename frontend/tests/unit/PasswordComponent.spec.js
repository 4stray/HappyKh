import { shallowMount } from '@vue/test-utils';
import PasswordComponent from '../../src/components/PasswordComponent.vue';

const expect = require('chai').expect;
const should = require('chai').should();

describe('Password data() check', () => {
    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('oldPassword');
    });

    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('newPassword1');
    });

    it('has userFirstName', () => {
        expect(PasswordComponent.data()).to.have.property('newPassword2');
    });
});

describe('Password mounted fields check', () => {
    const wrapper = shallowMount(PasswordComponent);

    it('has 3 fields with password type', () => {
        expect(wrapper.findAll('[type=password]').length).to.be.equal(3);
    });
});

describe('Django Server patch password', () => {
    it('has OK response to password change', () => {
        const request = new XMLHttpRequest();

        request.open('PATCH', 'http://localhost:8000/api/users/profile/5', false);

        request.setRequestHeader(
            "Content-type",
            'application/json; charset=utf-8',
        );

        request.setRequestHeader(
            "Authorization",
            'Token 1a0ccc1ff0455016164ddac9366af9c7711fe9ef'
        );

        request.send(JSON.stringify({old_password: 'admin', new_password1:'admin', new_password2:'admin'}));

        expect(request.status).to.be.equal(200);
    });
});