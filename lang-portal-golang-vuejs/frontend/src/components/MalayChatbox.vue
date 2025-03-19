<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>Malay Language Assistant</h1>
      <p>Practice your Malay with our AI language tutor</p>
    </div>
    
    <div class="chat-messages" ref="chatMessages">
      <div v-if="conversations.length === 0 || currentConversation.messages.length === 0" class="empty-state">
        <p>Start a conversation with your Malay language assistant!</p>
      </div>
      <div v-else v-for="(message, index) in currentConversation.messages" :key="index" 
           :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
        <div class="message-content">
          <p v-html="formatMessage(message.content)"></p>
        </div>
      </div>
      <div v-if="loading" class="message assistant-message">
        <div class="message-content">
          <p>Thinking...</p>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <textarea 
        v-model="userInput" 
        placeholder="Type your message here..." 
        @keyup.enter="sendMessage"
        :disabled="loading"
        ref="inputField"
      ></textarea>
      <button @click="sendMessage" :disabled="loading || !userInput.trim()">
        <span>Send</span>
      </button>
    </div>
    
    <div class="chat-controls">
      <div class="model-selector">
        <label for="model-select">AI Model:</label>
        <select id="model-select" v-model="selectedModel" @change="saveCurrentConversation">
          <option value="llama3">Llama 3</option>
          <option value="mistral">Mistral</option>
          <option value="gemma">Gemma</option>
        </select>
      </div>
      
      <div class="conversation-controls">
        <button @click="startNewConversation" class="control-button">
          New Chat
        </button>
        <select v-model="currentConversationId" @change="loadConversation">
          <option v-for="conv in conversations" :key="conv.id" :value="conv.id">
            {{ formatConversationTitle(conv) }}
          </option>
        </select>
        <button @click="deleteCurrentConversation" class="control-button delete">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: 'MalayChatbox',
  data() {
    return {
      userInput: '',
      loading: false,
      selectedModel: 'llama3',
      conversations: [],
      currentConversationId: '',
    };
  },
  computed: {
    currentConversation() {
      const conversation = this.conversations.find(c => c.id === this.currentConversationId);
      return conversation || { id: '', messages: [], model: this.selectedModel };
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.loading) return;
      
      // Add user message to chat
      const userMessage = {
        role: 'user',
        content: this.userInput.trim()
      };
      
      // Get current conversation
      const conversation = this.conversations.find(c => c.id === this.currentConversationId);
      if (conversation) {
        conversation.messages.push(userMessage);
      }
      
      // Clear input and set loading state
      const inputText = this.userInput;
      this.userInput = '';
      this.loading = true;
      
      try {
        // Query Ollama API
        const response = await this.queryOllama(inputText);
        
        // Add assistant response to chat
        if (conversation) {
          conversation.messages.push({
            role: 'assistant',
            content: response
          });
          
          // Save conversation
          this.saveCurrentConversation();
        }
      } catch (error) {
        console.error('Error querying Ollama:', error);
        if (conversation) {
          conversation.messages.push({
            role: 'assistant',
            content: 'Sorry, I encountered an error. Please try again later.'
          });
          this.saveCurrentConversation();
        }
      } finally {
        this.loading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
          this.resizeInput();
        });
      }
    },
    async queryOllama(prompt) {
      try {
        const url = 'http://localhost:11434/api/chat';
        const payload = {
          model: this.selectedModel,
          messages: [{ role: 'user', content: prompt }],
          stream: false
        };
        
        const response = await axios.post(url, payload);
        
        if (response.status === 200 && response.data && response.data.message) {
          return response.data.message.content;
        } else {
          return `Error: Unexpected response format`;
        }
      } catch (error) {
        console.error('API Error:', error);
        return `Error: ${error.message || 'Unknown error'}`;
      }
    },
    scrollToBottom() {
      const chatContainer = this.$refs.chatMessages;
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    },
    resizeInput() {
      const textarea = this.$refs.inputField;
      if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
      }
    },
    formatMessage(content) {
      return DOMPurify.sanitize(marked.parse(content));
    },
    // Conversation management
    generateId() {
      return Date.now().toString(36) + Math.random().toString(36).substring(2);
    },
    formatConversationTitle(conversation) {
      if (!conversation || !conversation.messages || conversation.messages.length === 0) {
        return 'New Conversation';
      }
      
      // Use the first user message as the title
      const firstUserMessage = conversation.messages.find(m => m.role === 'user');
      const title = firstUserMessage ? firstUserMessage.content : 'New Conversation';
      
      // Truncate and format the title
      return title.length > 25 ? title.substring(0, 25) + '...' : title;
    },
    saveCurrentConversation() {
      if (!this.currentConversationId) return;
      
      // Find the current conversation
      const conversationIndex = this.conversations.findIndex(c => c.id === this.currentConversationId);
      if (conversationIndex === -1) return;
      
      // Update the conversation
      this.conversations[conversationIndex] = {
        id: this.currentConversationId,
        model: this.selectedModel,
        messages: this.currentConversation.messages,
        lastUpdated: new Date().toISOString()
      };
      
      // Save to localStorage
      localStorage.setItem('malay-chatbox-conversations', JSON.stringify(this.conversations));
    },
    loadConversations() {
      try {
        const saved = localStorage.getItem('malay-chatbox-conversations');
        if (saved) {
          this.conversations = JSON.parse(saved);
        }
        
        // If no conversations exist, create a new one
        if (this.conversations.length === 0) {
          this.startNewConversation();
        } else {
          // Load the most recent conversation
          this.conversations.sort((a, b) => 
            new Date(b.lastUpdated) - new Date(a.lastUpdated)
          );
          this.currentConversationId = this.conversations[0].id;
          this.selectedModel = this.conversations[0].model || 'llama3';
        }
      } catch (error) {
        console.error('Error loading conversations:', error);
        this.startNewConversation();
      }
    },
    loadConversation() {
      const conversation = this.conversations.find(c => c.id === this.currentConversationId);
      if (conversation) {
        this.selectedModel = conversation.model || 'llama3';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    startNewConversation() {
      const newId = this.generateId();
      const newConversation = {
        id: newId,
        model: this.selectedModel,
        messages: [{
          role: 'assistant',
          content: 'Selamat datang! I\'m your Malay language assistant. How can I help you practice today?'
        }],
        lastUpdated: new Date().toISOString()
      };
      
      this.conversations.unshift(newConversation);
      this.currentConversationId = newId;
      
      // Save to localStorage
      localStorage.setItem('malay-chatbox-conversations', JSON.stringify(this.conversations));
      
      // Focus the input field
      this.$nextTick(() => {
        if (this.$refs.inputField) {
          this.$refs.inputField.focus();
        }
      });
    },
    deleteCurrentConversation() {
      if (this.conversations.length <= 1) {
        // If this is the only conversation, just clear it and create a new one
        this.startNewConversation();
        return;
      }
      
      // Remove the current conversation
      const index = this.conversations.findIndex(c => c.id === this.currentConversationId);
      if (index !== -1) {
        this.conversations.splice(index, 1);
        
        // Select another conversation
        this.currentConversationId = this.conversations[0].id;
        this.loadConversation();
        
        // Save to localStorage
        localStorage.setItem('malay-chatbox-conversations', JSON.stringify(this.conversations));
      }
    }
  },
  mounted() {
    this.loadConversations();
    this.$nextTick(() => {
      this.scrollToBottom();
      this.resizeInput();
      if (this.$refs.inputField) {
        this.$refs.inputField.focus();
      }
    });
  },
  watch: {
    userInput() {
      this.$nextTick(() => {
        this.resizeInput();
      });
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 85vh;
  max-width: 900px;
  margin: 2rem auto;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-header {
  padding: 1.5rem;
  background-color: #0066cc;
  color: white;
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.8rem;
}

.chat-header p {
  margin: 0.5rem 0 0;
  font-size: 1rem;
  opacity: 0.9;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #888;
  font-size: 1.1rem;
}

.chat-messages {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #f8f9fa;
}

.message {
  display: flex;
  margin-bottom: 1rem;
}

.user-message {
  justify-content: flex-end;
}

.assistant-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.user-message .message-content {
  background-color: #0066cc;
  color: white;
  border-radius: 12px 12px 0 12px;
}

.assistant-message .message-content {
  background-color: white;
  color: #333;
  border-radius: 12px 12px 12px 0;
}

.message-content p {
  margin: 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-content :deep(pre) {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.message-content :deep(code) {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}

.user-message .message-content :deep(pre),
.user-message .message-content :deep(code) {
  background-color: rgba(255, 255, 255, 0.2);
}

.chat-input {
  display: flex;
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

textarea {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  min-height: 60px;
  max-height: 150px;
  font-family: inherit;
  font-size: 1rem;
}

button {
  margin-left: 0.8rem;
  padding: 0 1.5rem;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #0055aa;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.chat-controls {
  padding: 1rem;
  background-color: #f8f9fa;
  border-top: 1px solid #e0e0e0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
}

.model-selector, .conversation-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.model-selector label {
  font-weight: 500;
}

select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-family: inherit;
}

.conversation-controls select {
  min-width: 200px;
}

.control-button {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.control-button:hover {
  background-color: #e0e0e0;
}

.control-button.delete {
  background-color: #fff0f0;
  color: #cc0000;
  border-color: #ffcccc;
}

.control-button.delete:hover {
  background-color: #ffe0e0;
}

@media (max-width: 768px) {
  .chat-container {
    margin: 1rem;
    height: 90vh;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .chat-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .model-selector, .conversation-controls {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
