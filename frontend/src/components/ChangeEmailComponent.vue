<template>
  <v-card class="v-card pa-5 mb-5">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Change your email</h3>
    </v-card-title>
    <v-form ref="form" @submit.prevent="changeEmail" v-model="valid">
      <v-text-field v-model="email"
                    :rules="emailRules"
                    label="New email"
                    required></v-text-field>
      <v-btn type="submit" :disabled="!valid" color="success" block
      >submit
      </v-btn>
    </v-form>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { axiosInstanceAuth } from '../axios-config';

export default {
  name: 'ChangeEmailComponent',
  computed: {
    ...mapGetters({
      userToken: 'getToken',
      userID: 'getUserID',
    }),
  },
  data() {
    return {
      valid: false,
      email: '',
      emailRules: [
        v => Boolean(v) || 'E-mail is required',
        v => /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(v)
          || 'E-mail must be valid',
      ],
    };
  },
  methods: {
    changeEmail() {
      if (!this.$refs.form.validate()) {
        this.$refs.form.reset();
        return;
      }
      const newEmail = { email: this.email };
      axiosInstanceAuth.patch(`/api/users/${this.userID}/email`, newEmail)
        .then(() => {
          this.$awn.success('Please check your mailbox for confirmation email');
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          }
        });
      this.$refs.form.reset();
    },
  },
};
</script>
<style scoped lang="scss">

</style>
