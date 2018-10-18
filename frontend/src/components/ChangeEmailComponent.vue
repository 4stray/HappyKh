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
import axios from 'axios';

const UserAPI = 'http://127.0.0.1:8000/api/users/';

export default {
  name: 'ChangeEmailComponent',
  data() {
    return {
      valid: false,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
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
      axios.patch(
        `${UserAPI + this.$cookies.get('user_id')}/email`,
        newEmail,
        {
          headers: { Authorization: `Token ${this.$cookies.get('token')}` },
        },
      ).then(() => {
        this.$awn.success('Please check your mailbox for confirmation email');
      })
        .catch((error) => {
          if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          } else {
            this.$awn.warning(error.message);
          }
        });
      this.$refs.form.reset();
    },
  },
};
</script>
<style scoped lang="scss">

</style>
