import router from '../../router';


export default {
  signout(context, redirect) {
    context.$cookies.remove('token');
    context.$cookies.remove('user_id');

    if (redirect) router.push(redirect);
    router.push({ name: 'home' });
  },

  getAuthenticationHeader(context) {
    return `Token ${context.$cookies.get('token')}`;
  },
};
