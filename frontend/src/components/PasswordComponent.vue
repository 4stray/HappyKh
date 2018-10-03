<template>
  <v-card class="v-card pa-4 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Change your password</h3>
    </v-card-title>
    <v-form ref="form" @submit.prevent="saveNewPassword" v-model="valid">
      <v-text-field type="password"
                    v-model="oldPassword"
                    label="Old password"
                    :rules="passwordRules"/>
      <v-text-field type="password"
                    v-model="newPassword"
                    label="New password"
                    :rules="passwordRules"/>
      <v-text-field type="password"
                    v-model="confirmationPassword"
                    :rules="[passwordRules, passwordsMatch]"
                    label="Confirm new password"/>
      <v-btn type="submit"
             :disabled="!valid"
             color="success"
      > submit
      </v-btn>
    </v-form>
  </v-card>
</template>

<script>
import axios from 'axios';
import Authentication from './Authentication/auth';

const UserAPI = 'http://127.0.0.1:8000/api/users/';

export default {
  name: 'PasswordComponent',
  components: {},
  data() {
    return {
      valid: true,
      oldPassword: '',
      newPassword: '',
      confirmationPassword: '',
      passwordRules: [
        value => !!value || 'This field is required.',
        value => value.length >= 8 || 'Your password must be at least 8 characters.',
        value => /^[0-9a-zA-Z]+$/.test(value) || 'Your password must contain only numbers and alphabetical characters.',
      ],
    };
  },
  methods: {
    passwordsMatch(confirmationPassword) {
      if (confirmationPassword.length < 0) {
        return false;
      }
      return this.newPassword === confirmationPassword || "Passwords don't match";
    },
    saveNewPassword() {
      if (!this.$refs.form.validate()) {
        this.$refs.form.reset();
      }
      const userCredentials = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
      };
      axios.patch(
        UserAPI + this.$cookies.get('user_id'), userCredentials,
        {
          headers: { Authorization: Authentication.getAuthenticationHeader(this) },
        },
      ).then(() => {
        this.$awn.success('Password successfully changed.');
      }).catch((error) => {
        if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        }
      });
      this.$refs.form.reset();
    },
  },
};
</script>

<style scoped>

</style>
