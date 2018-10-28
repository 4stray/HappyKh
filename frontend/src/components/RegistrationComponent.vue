<template>
  <v-form ref="form" @submit.prevent="register" v-model="valid">
    <div class="content">
      <v-text-field id="userEmail"
                    type="email"
                    v-model.trim="userEmail"
                    :rules="emailRules"
                    label="Email"></v-text-field>
      <v-text-field id="userName"
                    type="text"
                    v-model="userFirstName"
                    label="First name"
                    :rules="userNameRules"></v-text-field>
      <v-text-field id="userPassword"
                    type="password"
                    v-model="userPassword"
                    label="Password"
                    :rules="passwordRules"></v-text-field>
      <v-text-field id="confirmationPassword"
                    type="password"
                    v-model="confirmationPassword"
                    :rules="passwordRules"
                    label="Confirm your password"></v-text-field>
    </div>
    <input class="btn-submit" type="submit" :disabled="!valid"
           value="REGISTER"/>
  </v-form>
</template>

<script>
import axios from 'axios';

const UserAPI = 'http://localhost:8000/api/users';

export default {
  name: 'RegistrationComponent',
  data() {
    return {
      userEmail: '',
      userFirstName: '',
      userPassword: '',
      confirmPassword: '',
      valid: false,
      userNameRules: [
        value => Boolean(value) || 'This field is required.',
      ],
      passwordRules: [
        value => Boolean(value) || 'This field is required.',
        value => (value && value.length >= 8)
          || 'Your password must be at least 8 characters.',
        value => /^[0-9a-zA-Z]+$/.test(value)
          || 'Your password must contain only numbers ' +
          'and alphabetical characters.',
      ],
      emailRules: [
        v => Boolean(v) || 'E-mail is required',
        v => /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(v)
          || 'E-mail must be valid',
      ],
    };
  },
  methods: {
    register() {
      if (!this.$refs.form.validate()) {
        this.$refs.form.reset();
        return;
      } else if (this.userPassword !== this.confirmationPassword) {
        this.$awn.warning('Passwords don\'t match');
        this.$refs.form.reset();
        return;
      }
      const userCredentials = {
        user_email: this.userEmail,
        user_password: this.userPassword,
        first_name: this.userFirstName,
      };

      axios.post(`${UserAPI}/registration`, userCredentials)
        .then(() => {
          this.$awn.success('Successful registration.' +
            ' Please check your mailbox for confirmation email.');
          this.$router.push({name: 'home'});
        }).catch((error) => {
        if (error.response === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else if (error.response.status === 400) {
          this.$awn.alert(error.response.data.message);
        } else if (error.response.status === 500 && error.response.data.message) {
          this.$awn.info(error.response.data.message);
        }

        if (this.$cookies) {
          this.$cookies.remove('token');
          this.$cookies.remove('user_id');
        }
        this.$refs.form.reset();
      });
    },
  },
};
</script>

<style scoped lang="scss">

</style>
