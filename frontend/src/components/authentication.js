import axios from 'axios';
import querystring from 'querystring';

/**
 * @description Send user's credentials for authentication
 * @param {Component} context - Login Component
 * @param {Object} userCredentials
 */
function login(context, userCredentials) {
  axios.post(
    'http://localhost:8000/api/users/login/',
    querystring.stringify(userCredentials),
  )
    .then((response) => {
      if (response.data.status) {
        context.$router.push('/');
      } else {
        context.response = {
          message: response.data.message,
          status: response.data.status,
        };
      }
    }).catch((error) => {
      context.response = {
        message: error.message,
        status: false,
      };
    });
}

/**
 * @description Send user's credentials for registration
 * @param {Component} context - Login Component
 * @param userCredentials
 * @param redirect - redirect-rout after successful registration
 */
function register(context, userCredentials, redirect) {
  axios.post('http://localhost:8000/api/users/registration/', userCredentials)
    .then((response) => {
      context.$cookie.set('token', response.data.token);
      context.response = {
        message: response.data.message,
        status: response.data.status,
      };
      if (redirect) {
        context.$router.push(redirect);
      }
    }).catch((error) => {
      context.response = {
        message: error.message,
        status: false,
      };
      if (context.$cookie) {
        context.$cookie.delete('token'); // if the request fails, remove any possible user token if possible
      }
    });
}

export { login, register };
