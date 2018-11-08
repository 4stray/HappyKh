<script>
// @ is an alias to /src
import { axiosInstance } from '../axios-requests';

export default {
  name: 'ConfirmRegistrationComponent',
  created() {
    /* eslint-disable prefer-destructuring */
    const userId = this.$route.params.userId;
    const emailToken = this.$route.params.emailToken;

    axiosInstance.get(
      `/api/users/activate/${userId}/${emailToken}/`,
      {
        userId,
        emailToken,
      },
    ).then((response) => {
      /* eslint-disable-next-line no-console */
      console.log(response.status);
      this.$awn.success('Your account has been activated successfully');
    }).catch((error) => {
      if (error.response === undefined) {
        this.$awn.alert('A server error has occurred, try again later');
      } else {
        this.$awn.warning(error.response.data.message);
      }
    });
    this.$router.push({ name: 'login' });
  },
};
</script>
