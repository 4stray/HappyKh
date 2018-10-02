<template>
  <v-card class="v-card card-style">
    <v-card-title primary-title>
      <h3 class="headline mb-0">Change your email</h3>
    </v-card-title>
    <v-form aref="form" @submit.prevent="submit" v-model="valid">
      <v-text-field v-model="email"
                    :rules="emailRules"
                    label="Old email"
                    required/>
      <v-btn type="submit"
             :disabled="!valid"
             color="success"
      >submit
      </v-btn>
    </v-form>
  </v-card>
</template>

<script>
  import axios from "axios";

  export default {
    name: "ChangeEmailComponent",
    components: {},
    data: () => (
      {
        valid: true,
        email: '',
        emailRules: [
          v => !!v || 'E-mail is required',
          v => /.+@.+/.test(v) || 'E-mail must be valid'
        ],
      }),
    methods: {
      submit() {
        if (!this.$refs.form.validate()) {
          this.$refs.form.reset();
        }
        // Native form submission is not yet supported
        axios.patch('/api/profile/settings/email', {
          email: this.email,
        });

      }
    }
  }
</script>
<style scoped lang="scss">
  $primaryColor: #0ca086;
  .card-style {
    width: 70%;
    margin: 20px auto;
    padding: 30px 40px;
  }

</style>