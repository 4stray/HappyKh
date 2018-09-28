<template>
  <form id="confirmationEmail" method="post" @submit.prevent="sendEmail" novalidate>
    <div class="content">
      <input type="email" name="userEmail" v-model.trim="userEmail"
             placeholder="EMAIL"/>
    </div>
    <input class="btn-submit" type="submit" :disabled="isDisabledButton"
           value="SEND EMAIL"/>
  </form>
</template>

<script>
import Axios from 'axios';

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

      Axios.post('http://127.0.0.1:8000/api/users/activate/send-email/', userCredentials)
        .then(() => {
          this.$awn.success('Please check your mailbox for confirmation email')})
        .catch((error) => {
          this.$awn.warning(error.response.data.message)});

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
