<template>
    <v-flex xs12>
        <v-layout align-center justify-space-around row class="ma-3">
            <v-flex xs1 grow>
                <v-avatar size="65" color="indigo mr-4">
                    <img
                            class="avatar"
                            v-on:click="link"
                            :src="comment.creator_image"
                    >
                </v-avatar>
            </v-flex>
            <v-spacer></v-spacer>
            <v-flex xs10>
                <v-layout column>
                    <v-flex>
                        <v-layout justify-space-between >
                            <span class="subheading fullName">{{comment.creator_fullname}}</span>
                            <span class="body-2 creationDate">{{dateTime}}</span>
                        </v-layout>
                    </v-flex>
                    <p class="text-sm-left body-2 pt-2">{{comment.text}}</p>
                    <v-layout align-start justify-end row>
                        <span class="caption" v-if="edited">(edited)</span>
                        <v-btn fab flat small bottom v-on:click="updateComment">
                        <v-icon size="1.3em" dark>edit</v-icon>
                    </v-btn>
                        <v-btn fab flat small bottom v-on:click="deleteComment">
                        <v-icon size="1.3em" dark>delete</v-icon>
                    </v-btn>
                    </v-layout>
                </v-layout>
                <v-divider></v-divider>
            </v-flex>
        </v-layout>
    </v-flex>
</template>

<script>
export default {
  name: 'CommentComponent',
  methods: {
    link() {
      this.$router.push({ name: 'profile', params: { id: this.comment.creator } });
    },
    deleteComment() {
      this.$parent.$emit('deleteComment', this.comment);
    },
    updateComment(){
      this.$parent.$emit('updateComment', this.comment);
    }
  },
  computed: {
    dateTime() {
      return this.comment.creation_time.slice(0, 19);
    },
  },
  props: {
    comment: {
      type: Object,
      default() {
        return {
          id: '',
          creation_time: '',
          text: '',
          creator: '',
          place: '',
          creator_image: '',
          creator_fullname: '',
          edited: false
        };
      },
    },
  },
};

</script>

<style scoped>
    .avatar:hover{
        cursor: pointer;
    }
    p{
        text-overflow: ellipsis;
        overflow: hidden;
    }
</style>
