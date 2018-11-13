<template>
    <v-container>
        <v-layout column>
            <v-flex xs12 v-if="pageDifference">
                <v-form @submit.prevent="upload">
                    <v-btn class="upload-button" color="#9cbbed" type="submit">
                        View {{commentsNotLoad}} more
                    </v-btn>
                </v-form>
            </v-flex>
            <CommentComponent v-for="comment in allComments"
                              v-bind:comment="comment"
                              :key="comment.id"/>
            <v-flex xs12>
                <v-layout column>
                    <v-form enctype="multipart/form-data"
                            @submit.prevent="leftComment">
                        <v-textarea
                                row-height="20"
                                rows="4"
                                v-model="newComment"
                                color="#010305"
                                label="Left your comment here"
                        ></v-textarea>
                        <v-flex xs12>
                            <v-layout row align-left>
                                <v-btn color="#0b563d" type="submit">Submit</v-btn>
                            </v-layout>
                        </v-flex>
                    </v-form>
                </v-layout>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import CommentComponent from './CommentComponent.vue';
import { getComments, axiosInstance } from '../axios-requests';


export default {
  name: 'CommentsCollectionComponent',
  components: {
    CommentComponent,
  },
  computed: {
    pageDifference() {
      return (this.numberOfPages - this.page > 0);
    },
    commentsNotLoad() {
      return this.count - (this.page * this.objects_per_page);
    },
  },
  methods: {
    leftComment() {
      if (this.newComment.length >= 4) {
        const formData = new FormData();
        const id = this.$route.params.id;
        formData.set('creator', this.$store.getters.getUserID);
        formData.set('place', id);
        formData.set('text', this.newComment);
        this.newComment = '';
        axiosInstance.post(
          `/api/places/${id}/comments`, formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          },
        ).then((response) => {
          this.$awn.success('Your comment was left.');
          this.allComments.push(response.data);
        }).catch((error) => {
          if (error.message === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.warning(this.error.message);
          }
        });
      }
    },
    upload() {
      const id = this.$route.params.id;
      this.page += 1;
      const params = {
        params: {
          objects_per_page: this.objects_per_page,
          page: this.page,
        },
      };
      getComments(id, params)
        .then((response) => {
          const responseData = response.data.comments;
          for (let i = 0; i < responseData.length; i += 1) {
            this.allComments.unshift(responseData[i]);
          }
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.alert(error);
          }
          this.page -= 1;
        });
    },
  },
  data() {
    return {
      allComments: [],
      page: 1,
      count: 0,
      numberOfPages: 1,
      objects_per_page: 3,
      newComment: '',
    };
  },
  created() {
    const id = this.$route.params.id;
    const params = {
      params: {
        objects_per_page: this.objects_per_page,
        page: this.page,
      },
    };
    getComments(id, params)
      .then((response) => {
        this.allComments = response.data.comments.reverse();
        this.numberOfPages = response.data.number_of_pages;
        this.count = response.data.count;
      }).catch((error) => {
        if (error.response === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else {
          this.$awn.alert(error);
        }
      });
  },
};
</script>

<style scoped>
    .upload-button {
        width: 100%;
        opacity: 0.5;
    }
</style>
