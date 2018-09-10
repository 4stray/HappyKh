<template>
    <form id="register" @submit.prevent="register">
        <div id="content">
            <input type="email" v-model.trim="userEmail" placeholder="EMAIL"/>
            <p v-if="errors.email" class="error">{{errors.email}}</p>
            <input id="password" type="password" v-model="userPassword" placeholder="PASSWORD"/>
            <input type="password" v-model="confirmPassword" placeholder="CONFIRM PASSWORD"/>
            <ul v-if="errors.password.length">
                <li v-for="(error, index) in errors.password" :key="index" class="error">{{ error }}</li>
            </ul>
        </div>
        <input id="btn-registration" type="submit" :disabled="isDisabled" value="SIGN UP"/>
    </form>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "RegistrationComponent",
        data() {
            return {
                userEmail: '',
                userPassword: '',
                confirmPassword: '',
                errors: {
                    email: '',
                    password: [],
                },
            };
        },
        computed: {
            isDisabled: function () {
                return !(this.userEmail && this.userPassword && this.confirmPassword);
            }
        },
        methods: {
            register: function () {
                if (this.validation()) {
                    const userCredentials = {
                        user_email: this.userEmail,
                        user_password: this.userPassword,
                    };
                    axios.post('http://localhost:8000/api/users/registration/', userCredentials)
                        .then((response) => {
                            if (response.data.status) {
                                this.$router.push('/');
                            } else {
                                this.$emit('serverResponse', response.data.message);
                            }
                        }).catch((error) => {
                        this.$emit('serverResponse', error);
                    });
                }
            },
            validation: function () {
                this.errors = {
                    email: '',
                    password: [],
                };
                if (!this.validEmail(this.userEmail)) {
                    this.errors.email = "* Please enter a valid email address.";
                }
                if (this.userPassword.length < 8) {
                    this.errors.password.push("* Your password must be at least 8 characters.");
                }
                const alphaNumeric = /^[0-9a-zA-Z]+$/;
                if (!this.userPassword.match(alphaNumeric)) {
                    this.errors.password.push("* Your password must contain only numbers and alphabetical characters.");
                }
                if (this.userPassword !== this.confirmPassword) {
                    this.errors.password.push("* Your passwords don't match, please try again.");
                }
                if (this.errors.length) {
                    return false;
                }
                return true;
            },
            validEmail: function (email) {
                const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(email);
            },
        },
    };
</script>

<style scoped lang="scss">
    #content {
        height: 240px;
        flex: 1 1 auto;

        input {
            background-color: transparent;
            border: none;
            border-bottom: 2px solid #ff8383;
            font-size: 16px;
            margin: 15px 0;
            outline: none;
            width: 100%;
        }

        input:focus {
            border-bottom: 2px solid #b71c1c;
        }
    }

    #btn-registration:disabled {
        background-color: #d3d3d3;
    }

    #btn-registration {
        width: 100%;
        color: #fff;
        background-color: #ffb6c1;
        border: none;
        padding: 10px 25px;
        margin: 5px 0;
        text-transform: uppercase;
        font-weight: 600;
        font-family: 'Liberation Sans', sans;
        cursor: pointer;
    }

    .error {
        color: #dc143c;
        font-size: 10px;
        font-family: 'Liberation Sans', sans, sans-serif;
        margin: 2px 0;
    }

    ul {
        padding: 0;
        margin: 0;
    }

    li {
        list-style: none;
    }

    label {
        color: #dc143c;
        margin: 2px 0;
    }
</style>
