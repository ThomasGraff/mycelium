<template>
  <div class="message-container" :class="{ 'user-message': isUser }">
    <div class="message-bubble" :class="{ 'user-bubble': isUser, 'ai-bubble': !isUser }">
      <v-card-text>
        <div v-html="renderedMarkdown"></div>
      </v-card-text>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { marked } from 'marked'

export default {
  name: 'ResultBox',
  props: {
    result: {
      type: String,
      required: true
    },
    isUser: {
      type: Boolean,
      default: false
    }
  },
  setup (props) {
    const renderedMarkdown = computed(() => {
      return marked(props.result)
    })

    return {
      renderedMarkdown
    }
  }
}
</script>

<style scoped>
.message-container {
  display: flex;
  margin-bottom: 16px;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-message {
  justify-content: flex-end;
}

.user-bubble {
  background-color: rgb(33, 33, 33);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-bubble {
  background-color: #F0F0F0;
  color: black;
  border-bottom-left-radius: 4px;
}

/* Add styles for markdown rendering */
:deep(ul), :deep(ol) {
  padding-left: 20px;
  margin: 0;
}

:deep(p) {
  margin-bottom: 8px;
  margin-top: 0;
}

:deep(li) {
  margin-bottom: 4px;
}
</style>
