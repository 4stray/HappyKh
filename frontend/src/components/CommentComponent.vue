<template>
    <v-flex xs12>
        <v-layout align-center justify-space-around row class="commentItem ma-3">
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
                        <v-layout justify-space-between row>
                            <span class="subheading">{{comment.creator_fullname}}</span>
                            <span class="body-2">{{date}}</span>
                        </v-layout>
                    </v-flex>
                    <p class="text-sm-left body-2 pt-2">{{comment.text}}</p>
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
  },
  computed: {
    date() {
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
    .commentItem{
        transition: 1s;
    }
</style>
