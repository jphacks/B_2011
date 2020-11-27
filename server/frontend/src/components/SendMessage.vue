<template>
  <div id="chat">
    <v-text-field
      v-model="message"
      label="受験者にメッセージを送信"
      type="text"
      @input="updateText($event)"
      clearable
    >
      <template v-slot:append-outer>
        <v-btn color="primary" @click="send">送信</v-btn>
      </template>
    </v-text-field>
  </div>
</template>

<style scoped>
  /deep/ .v-text-field{
    width: 700px;
  }
</style>

<script>
export default {
  name: 'SendMessage',
  methods: {
    updateText (text) {
      this.inputText = text
    },
    send () {
      this.$socket.send(JSON.stringify({ message: this.inputText }))
    }
  },
  data () {
    return {
      inputText: undefined
    }
  }
}

</script>
