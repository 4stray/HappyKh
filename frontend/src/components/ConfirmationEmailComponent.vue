<template>
  <v-form id="confirmationEmail" method="post" @submit.prevent="sendEmail"
        novalidate>
    <div class="content">
      <v-text-field type="email" name="userEmail" v-model.trim="userEmail"
                    label="Email"></v-text-field>
    </div>
    <input class="btn-submit" type="submit" :disabled="isDisabledButton"
           value="SEND EMAIL"/>
  </v-form>
</template>

<script>
import { axiosInstance } from '../axios-requests';

export default {
  name: 'ConfirmationEmailComponent',
  data() {
    return {
      userEmail: '',

    };
  },
  methods: {
    sendEmail() {
      const userCredentials = { user_email: this.userEmail };

      axiosInstance.post('/api/users/activate/send-email/', userCredentials)
        .then(() => {
          this.$awn.success('Please check your mailbox for confirmation email');
        })
        .catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.warning(error.response.data.message);
          }
        });

      this.userEmail = '';
    },
    isEmailValid() {
      const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return re.test(this.userEmail);
    },
  },
  computed: {
    /**
     * @description Checks if user filled all fields
     * @returns {boolean}
     * */
    isDisabledButton() {
      return !(this.isEmailValid());
    },
  },
};
</script>

<style scoped lang="scss">
</style>
