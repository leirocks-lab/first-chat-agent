<script setup>
import { ref } from 'vue'

const userInput = ref('')
const messages = ref([])
const loading = ref(false)

async function sendMessage() {
  if (!userInput.value.trim()) return
  const content = userInput.value
  messages.value.push({ role: 'user', content })
  userInput.value = ''
  loading.value = true
  try {
    const res = await fetch(`http://localhost:8000/chat?message=${encodeURIComponent(content)}`)
    const data = await res.text()
    messages.value.push({ role: 'ai', content: data })
  } catch (e) {
    messages.value.push({ role: 'ai', content: '请求失败，请重试。' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, idx) in messages" :key="idx" :class="['message', msg.role]">
        <span class="role">{{ msg.role === 'user' ? '你' : 'AI' }}：</span>
        <span class="content">{{ msg.content }}</span>
      </div>
      <div v-if="loading" class="message ai"><span class="role">AI：</span><span class="content">正在思考...</span></div>
    </div>
    <div class="input-area">
      <input v-model="userInput" @keyup.enter="sendMessage" placeholder="请输入你的问题..." :disabled="loading" />
      <button @click="sendMessage" :disabled="loading || !userInput.trim()">发送</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
}
.messages {
  min-height: 200px;
  margin-bottom: 1rem;
  max-height: 400px;
  overflow-y: auto;
}
.message {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: flex-start;
}
.message.user .role {
  color: #646cff;
}
.message.ai .role {
  color: #42b883;
}
.role {
  font-weight: bold;
  margin-right: 0.5em;
}
.input-area {
  display: flex;
  gap: 0.5rem;
}
input[type="text"] {
  flex: 1;
  padding: 0.5em;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1em;
}
button {
  padding: 0.5em 1.2em;
  border-radius: 4px;
  border: none;
  background: #646cff;
  color: #fff;
  font-size: 1em;
  cursor: pointer;
  transition: background 0.2s;
}
button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style> 