<template>
    <v-layout align-center justify-start row class="ma-3">
        <v-flex xs2>
                <v-avatar size="65" color="indigo mr-4" >
                    <img
                       class="avatar"
                       v-on:click="link"
                       :src="comment.auth.avatar"
                    >
                </v-avatar>
        </v-flex>
        <v-flex>
            <v-layout column>
                <v-flex>
                    <v-layout justify-space-between row>
                        <span class="subheading">{{comment.auth.fullName}}</span>
                        <span class="body-2">{{comment.self.date}}</span>
                    </v-layout>
                </v-flex>
                <p class="text-sm-left body-2 pt-2">{{comment.self.text}}</p>
            </v-layout>
            <v-divider></v-divider>
        </v-flex>
    </v-layout>
</template>

<script>
export default {
  name: 'CommentComponent',
  methods: {
    link() {
      this.$router.push({ name: 'profile', params: { id: this.comment.auth.id } });
    },
  },
  props: {
    comment: {
      type: Object,
      default() {
        return {
          auth: {
            id: '',
            fullName: '',
            avatar: '',
          },
          self: {
            id: '',
            text: '',
            date: '',
          },
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
</style>
