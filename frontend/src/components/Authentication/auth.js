import Axios from 'axios';
import router from '../../router';

const UserAPI = 'http://127.0.0.1:8000/api/users';

export default {
  user: {authenticated: false},

  authenticate(context, credentials, redirect) {
    Axios.post(`${UserAPI}/login/`, credentials)
        .then((response) => {
          context.$cookies.set('token', response.data['token']);
          context.$cookies.set('user_id', response.data['user_id']);

          this.user.authenticated = true;

          if (redirect) router.push(redirect);
        }).catch((error) => {
          if (error.response.data.message) {
            context.$awn.warning(error.response.data.message);
          }
          this.signout(this);
          context.$awn.warning(context.error.message);
        });
  },

  signout(context, redirect) {
    context.$cookies.remove('token');
    context.$cookies.remove('user_id');
    this.user.authenticated = false;

    if (redirect) router.push(redirect);
    router.push({ name: 'home' });
  },

  checkAuthentication() {
    const token = document.cookie;
    this.user.authenticated = !!token;
  },

  getAuthenticationHeader(context) {
    return 'Token ' + context.$cookies.get('token');
  },
};