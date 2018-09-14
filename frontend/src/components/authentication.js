import axios from 'axios';
import querystring from 'querystring';

/**
 * @description Checks correctness of  user's email
 * @param {string} email
 * @returns {*|boolean}
 */
function isEmailValid(email) {
  const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  return re.test(email);
}

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
  console.log(userCredentials);
  axios.post('http://localhost:8000/api/users/registration/', userCredentials)
    .then((response) => {
      context.response = {
        message: response.data.message,
        status: response.data.status,
      };
      if (redirect) {
        context.$router.push(redirect);
      }
    }).catch((error) => {
      console.log('Error register');
      context.response = {
        message: error.message,
        status: false,
      };
      if (context.$cookies) {
        context.$cookies.remove('token');
        // if the request fails, remove any possible user token if possible
      }
    });
}

// export { login, register, isEmailValid };
