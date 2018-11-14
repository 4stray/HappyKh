<template>
  <v-layout justify-space-around row fill-height>
    <v-flex xs12 mt-4>
      <v-layout justify-start column>
          <v-label class="d-block" id="labelRating">Rate this place:</v-label>
          <v-rating
              id="placeRating"
              v-model="rating"
              background-color="orange lighten-3"
              color="orange"
              :halfIncrements=true
              :hover=true>
          </v-rating>
          <v-btn
              id="rating-btn"
              color="primary"
              v-on:click="save()"
              flat>
            Rate Now
          </v-btn>
      </v-layout>
    </v-flex>
  </v-layout>
</template>
<script>
import { mapGetters } from 'vuex';
import { axiosInstance, getPlaceRating } from '../axios-requests';

export default {
  name: 'PlaceRatingComponent',
  computed: {
    ...mapGetters({
      userToken: 'getToken',
      userID: 'getUserID',
    }),
  },
  data() {
    return {
      rating: 0,
    };
  },
  created() {
    this.fetchRating();
  },
  methods: {
    fetchRating() {
      getPlaceRating(this.$route.params.id).then((response) => {
        this.rating = response.data.rating;
      }).catch((error) => {
        if (error.response === undefined) {
          this.$awn.alert('A server is currently unavailable');
        } else if (error.response.data.message) {
          this.$awn.warning(error.response.data.message);
        } else if (error.status === 404) {
          this.rating = 0;
        }
      });
    },
    save() {
      const ratingData = {
        user: this.userID,
        place: this.$route.params.id,
        rating: this.rating,
      };
      axiosInstance.post(`/api/places/rating/${this.$route.params.id}`, ratingData)
        .then((response) => {
          this.rating = response.data.rating;
          this.$awn.success('The place was successfully rated.');
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server is currently unavailable');
          } else if (error.response.data.message) {
            this.$awn.warning(error.response.data.message);
          } else if (error.response.status === 400) {
            this.$awn.warning('An error occurred');
          }
        });
    },
  },
};
</script>
