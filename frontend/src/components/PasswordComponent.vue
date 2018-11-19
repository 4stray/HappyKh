<template>
  <v-card class="v-card pa-5 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Change your password</h3>
    </v-card-title>
    <v-form ref="form" @submit.prevent v-model="valid">
      <v-text-field type="password"
                    v-model="oldPassword"
                    label="Old password"
                    :rules="passwordRules"></v-text-field>
      <v-text-field type="password"
                    v-model="newPassword"
                    label="New password"
                    :rules="passwordRules"></v-text-field>
      <v-text-field name="confirmationPassword"
                    type="password"
                    v-model="confirmationPassword"
                    :rules="passwordRules"
                    label="Confirm new password"></v-text-field>
      <v-btn type="submit"
             v-on:click.native="saveNewPassword"
             :disabled="!valid"
             color="success" block>
        submit
      </v-btn>
    </v-form>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { axiosInstance } from '../axios-requests';

export default {
  name: 'PasswordComponent',
  computed: {
    ...mapGetters({
      userToken: 'getToken',
      userID: 'getUserID',
    }),
  },
  data() {
    return {
      valid: false,
      oldPassword: '',
      newPassword: '',
      confirmationPassword: '',
      passwordRules: [
        value => Boolean(value) || 'This field is required.',
        value => (value && value.length >= 8)
          || 'Your password must be at least 8 characters.',
        value => /^[0-9a-zA-Z]+$/.test(value)
          || 'Your password must contain only numbers ' +
          'and alphabetical characters.',
      ],
    };
  },
  methods: {
    signOut() {
      this.$store.dispatch('signOut').finally(() => {
        this.$awn.success('You have successfully changed your password.');
        this.$router.push({ name: 'login' });
      });
    },
    saveNewPassword() {
      if (!this.$refs.form.validate() || this.oldPassword === this.newPassword) {
        this.$refs.form.reset();
        this.$awn.warning('Some passwords were invalid');
        return;
      }
      if (this.newPassword !== this.confirmationPassword) {
        this.$awn.warning('Passwords don\'t match');
        this.$refs.form.reset();
        return;
      }
      const userCredentials = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
      };

      axiosInstance.patch(`/api/users/${this.userID}/password`, userCredentials)
        .then(() => {
          this.signOut();
        })
        .catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          }
          this.$refs.form.reset();
        });
    },
  },
};
</script>

<style scoped>

</style>
