  <template>
  <LoginComponent/>
</template>

<script>
import LoginComponent from '../components/LoginComponent.vue';

export default {
  name: 'Login',
  data() {
    return {
      input: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      /* Validation */
    },
  },
  components: {
    LoginComponent,
  },
};
</script>

<style scoped>
</style>
