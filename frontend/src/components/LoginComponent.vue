<template>
  <form id="login"
        @submit.prevent="login"
        action="/home"
        method="post"
        novalidate>
    <div id="content">
      <input type="email" name="username" v-model.trim="userEmail" placeholder="EMAIL"/>
      <input type="password" name="password" v-model="userPassword" placeholder="PASSWORD"/>
    </div>
    <input id="btn-login" type="submit" :disabled="isDisabled" value="Login"/>
  </form>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'LoginComponent',
        data() {
            return {
                userEmail: '',
                userPassword: '',
            };
        },
        computed: {
            isDisabled: function () {
                return !(this.validEmail(this.userEmail) && this.userPassword)
            }
        },
        methods: {
            login() {
                const userCredentials = {
                    user_email: this.userEmail,
                    user_password: this.userPassword,
                };
                axios.post('http://localhost:8000/api/users/login/', userCredentials)
                    .then((response) => {
                        if (response.data.status) {
                            this.$router.push('/');
                        } else {
                            console.exception(response.data.message);
                            this.$emit('serverResponse', response.data.message)
                        }
                    }).catch((error) => {
                    console.error(error);
                    this.$emit('serverResponse', error)
                });
            },
            validEmail: function (email) {
                const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(email);
            },
        },
    };
</script>

<style scoped lang="scss">
  #login {
    display: flex;
    flex-direction: column;
    height: 80%;
  }

  #content {
    height: 200px;
    flex: 1 1 auto;

    input {
      background-color: transparent;
      border: none;
      border-bottom: 2px solid #ff8383;
      font-size: 16px;
      outline: none;
      margin: 15px 0;
      width: 100%;
    }

    input:focus {
      border-bottom: 2px solid #b71c1c;
    }
  }

  #btn-login {
    width: 100%;
    border: none;
    padding: 10px 25px;
    color: #fff;
    text-transform: uppercase;
    font-weight: 600;
    font-family: 'Liberation Sans', sans, sans-serif;
    cursor: pointer;
    background-color: #ffb6c1;
  }

  #btn-login:disabled {
    background-color: #d3d3d3;
  }
</style>
