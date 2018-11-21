<template>
        <v-layout column>
            <v-flex xs12 v-if="pageDifference">
                <v-form @submit.prevent="upload">
                    <v-btn id="uploadButton" color="#9cbbed" type="submit">
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
                            @submit.prevent="leaveComment">
                        <v-textarea
                                ref="commentText"
                                id="newCommentInput"
                                row-height="20"
                                rows="4"
                                v-model="newComment"
                                label="Leave your comment here"
                        ></v-textarea>
                        <v-flex xs12>
                            <v-layout row align-left>
                                <v-btn id="postCommentBtn"
                                       color="#4286f4"
                                       type="submit">Submit</v-btn>
                            </v-layout>
                        </v-flex>
                    </v-form>
                </v-layout>
            </v-flex>
        </v-layout>
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
    leaveComment() {
      if (this.commentToUpdate) this.updateComment();
      else if (this.newComment.length >= 4) {
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
    deleteComment(comment) {
      const id = this.$route.params.id;
      axiosInstance.delete(
        `/api/places/${id}/comments/${comment.id}`,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then(() => {
        this.$awn.success('Your comment was deleted.');
        const index = this.allComments.indexOf(comment);
        if (index !== -1) this.allComments.splice(index, 1);
      }).catch((error) => {
        if (error.message === undefined) {
          this.$awn.alert('A server error has occurred, try again later');
        } else {
          this.$awn.warning(this.error.message);
        }
      });
    },
    updateComment() {
      if (this.newComment.length >= 4) {
        const formData = new FormData();
        const id = this.$route.params.id;
        formData.set('creator', this.$store.getters.getUserID);
        formData.set('place', id);
        formData.set('text', this.newComment);
        this.newComment = '';
        axiosInstance.put(
          `/api/places/${id}/comments/${this.commentToUpdate.id}`, formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          },
        ).then((response) => {
          this.$awn.success('Your comment was updated.');
          const index = this.allComments.indexOf(this.commentToUpdate);
          this.allComments.splice(index, 1, response.data);
          this.commentToUpdate = '';
        }).catch((error) => {
          if (error.message === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.warning(this.error.message);
          }
          this.commentToUpdate = '';
        });
      }
    },
    pushComments(responseData) {
      for (let i = 0; i < responseData.length; i += 1) {
        this.allComments.unshift(responseData[i]);
      }
    },
    getRequestParams() {
      return {
        params: {
          objects_per_page: this.objects_per_page,
          page: this.page,
        },
      };
    },
    upload() {
      const id = this.$route.params.id;
      this.page += 1;
      const params = this.getRequestParams();
      getComments(id, params)
        .then((response) => {
          const responseData = response.data.comments;
          this.pushComments(responseData);
        }).catch((error) => {
          if (error.response === undefined) {
            this.$awn.alert('A server error has occurred, try again later');
          } else {
            this.$awn.alert(error);
          }
          this.page -= 1;
        });
    },
    fetchCommentsCollectionData() {
      const id = this.$route.params.id;
      const params = this.getRequestParams();
      getComments(id, params)
        .then((response) => {
          this.pushComments(response.data.comments);
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
    setFocus(comment) {
      this.commentToUpdate = comment;
      this.$refs.commentText.value = comment.text;
      this.$refs.commentText.focus();
    },
  },
  data() {
    return {
      commentToUpdate: '',
      allComments: [],
      page: 1,
      count: 0,
      numberOfPages: 1,
      objects_per_page: 3,
      newComment: '',
    };
  },
  created() {
    this.fetchCommentsCollectionData();
    this.$on('deleteComment', this.deleteComment);
    this.$on('updateComment', this.setFocus);
  },
};
</script>

<style scoped>
    #uploadButton {
        width: 100%;
        opacity: 0.5;
    }
</style>
