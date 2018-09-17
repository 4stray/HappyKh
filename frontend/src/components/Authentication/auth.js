import Axios from 'axios';
import router from '../../router';

const UserAPI = 'http://127.0.0.1:8000/api/users';

export default {
  user: {authenticated: false},

  authenticate(context, credentials, redirect) {
    Axios.post(`${UserAPI}/login/`, credentials)
        .then((response) => {
            context.$cookies.set('token', response.data['token']);
            console.log(response.data['token']);
            context.$cookies.set('user_id', response.data['user_id']);

            this.user.authenticated = true;

            if (redirect) router.push(redirect);
        }).catch((error) => {
          alert(error);
        })  ;
  },

  // signup(context, credentials, redirect) {
  //   Axios.post(`${UserAPI}/v1/signup`, credentials)
  //       .then(() => {
  //         context.validSignUp = true;
  //
  //         this.authenticate(context, credentials, redirect);
  //       }).catch((error) => {
  //         alert(error);
  //       });
  // },

  signout(context, redirect) {
    context.$cookies.delete('token');
    context.$cookies.delete('user_id');
    this.user.authenticated = false;

    if (redirect) router.push(redirect);
  },

  checkAuthentication() {
    const token = document.cookie;
    this.user.authenticated = !!token;
  },

  getAuthenticationHeader(context) {
    return 'Token ' + context.$cookies.get('token');
  },
};