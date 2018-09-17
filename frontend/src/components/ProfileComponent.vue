<template>
  <div id="ProfileComponent">
    <h1>Your profile:</h1>
    <input type="text" :disabled="isDisabled" id="first_name"
           v-model="userFirstName" placeholder="First name"/>
    <input type="text" :disabled="isDisabled" id="last_name"
           v-model="userLastName" placeholder="Last name"/>
    <input type="number" :disabled="isDisabled" id="age" v-model="userAge" placeholder="Age"/>
    <select :disabled="isDisabled" v-model="userGender">
      <option disabled value="">Choose your gender</option>
      <option>Male</option>
      <option>Woman</option>
    </select>
    <input type="text" :disabled="isDisabled" id="email" v-model="userEmail" placeholder="Email"/>
    <img v-bind:src=userImage id='image' alt="внедренная иконка папки"/>
    <input type="file" id="imageInput" :disabled="isDisabled" v-on:change="changeImage()" accept="image/*"/>
    <button class="btn-change" v-on:click=edit()>{{ enableText }}</button>
    <button class="btn-save" type="button" v-on:click="save()">Save changes</button>
  </div>
</template>

<script>
import axios from 'axios';
import Authentication from '../components/Authentication/auth';

export default {
  name: 'ProfileComponent',
  data() {
    return {
      userFirstName: '',
      userLastName: '',
      userAge: '',
      userGender: 'Male',
      userEmail: '',
      userImage: '',
      isDisabled: true,
      enableText: 'Enable editing',
    };
  },
  created() {
    this.fetchUserCredentials();
  },
  methods: {
    fetchUserCredentials() {
      console.log(this.$cookies.get('token'));
      axios.get('http://localhost:8000/api/users/'+this.$cookies.get('user_id'),
          {
            headers: {'Authorization': Authentication.getAuthenticationHeader(this)},
          })
          .then((response) => {
              this.userFirstName = response.data['first_name'];
              this.userLastName = response.data['last_name'];
              this.userAge = response.data['age'];
              this.userGender = response.data['gender'];
              this.userEmail = response.data['email'];
              this.userImage = response.data['image'];
          }).catch((error) => {
        alert(error);
      });
    },
    save() {
      const userCredentials = {
        first_name: this.userFirstName,
        last_name: this.userLastName,
        age: this.userAge,
        gender: this.userGender,
        email: this.userEmail,
        image: this.userImage,
      };

      axios.patch('http://localhost:8000/api/users/'+this.$cookies.get('user_id'), userCredentials,
          {
            headers: {'Authorization': Authentication.getAuthenticationHeader(this)},
          })
          .then((response) => {
              this.isDisabled = true;
              this.enableText = 'Enable editing';
              this.userFirstName = response.data['first_name'];
              this.userLastName = response.data['last_name'];
              this.userAge = response.data['age'];
              this.userGender = response.data['gender'];
              this.userEmail = response.data['email'];
              this.userImage = response.data['image'];
              alert('Your profile was successfully updated.');
          }).catch((error) => {
        alert(error);
      });
    },
    edit() {
      this.isDisabled = !this.isDisabled;
      if (this.isDisabled) {
        this.enableText = 'Enable editing';
      } else {
        this.enableText = 'Disable editing';
      }
    },
    changeImage() {
      var file = document.getElementById('imageInput').files[0];
      var reader = new FileReader();

      var self = this;
      reader.addEventListener("load", function () {
        self.userImage = reader.result;
      }, false);

      reader.readAsDataURL(file);
    },
  },
};
</script>

<style scoped>
  #ProfileComponent {
    width: 500px;
    border: 1px solid #CCCCCC;
    background-color: #FFFFFF;
    margin: auto;
    margin-top: 130px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  input:focus {
    outline: none;
  }

  img {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 300px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  select {
    padding: 10px 15px;
    margin-bottom: 10px;
    width: 332px;
    height: 35px;
    border: 1px solid #ccc;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
  }

  .btn-change {
    margin-top: 5px;
    background-color: #ffc107;
    color: #fff;
    border: none;
    padding: 10px 25px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: "Liberation Sans", sans;
    border-radius: 20px;
    cursor: pointer;
  }

  .btn-change:hover {
    background-color: #ffa000;
  }

  .btn-save {
    margin-top: 5px;
    background-color: #ffc107;
    color: #fff;
    border: none;
    padding: 10px 25px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: "Liberation Sans", sans;
    border-radius: 20px;
    cursor: pointer;
  }

  .btn-save:hover {
    background-color: #ffa000;
  }
</style>
