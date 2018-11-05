<template>
  <v-form ref="form" @submit.prevent="login" v-model="valid">
    <div class="content">
      <v-text-field v-model="userEmail"
                    name="userEmail"
                    :rules="emailRules"
                    label="Email"></v-text-field>
      <v-text-field type="password"
                    v-model="userPassword"
                    name="userPassword"
                    label="Password"
                    :rules="passwordRules"></v-text-field>
    </div>
    <input class="btn-submit" type="submit" :disabled="!valid" value="LOGIN"/>
  </v-form>
</template>

<script>
import { axiosInstance } from '../axios-config';

export default {
  name: 'LoginComponent',
  data() {
    return {
      userEmail: '',
      userPassword: '',
      valid: false,
      passwordRules: [
        value => Boolean(value) || 'This field is required.',
        value => (value && value.length >= 8)
          || 'Your password must be at least 8 characters.',
      ],
      emailRules: [
        v => Boolean(v) || 'E-mail is required',
        v => /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(v)
          || 'E-mail must be valid',
      ],
    };
  },
  methods: {
    login() {
      const userCredentials = {
        user_email: this.userEmail,
        user_password: this.userPassword,
      };

      axiosInstance.post('/api/users/login', userCredentials)
        .then((response) => {
          this.$cookies.set('token', response.data.token);
          this.$store.commit('setAuthenticated', response.data.token);
          this.$cookies.set('user_id', response.data.user_id);
          this.$store.commit('setUserID', response.data.user_id);
          this.$router.push({ name: 'home' });
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          }
          this.$cookies.remove('token');
          this.$cookies.remove('user_id');
        });
      this.$refs.form.reset();
    },
  },
};
</script>

<style scoped lang="scss">

</style>
