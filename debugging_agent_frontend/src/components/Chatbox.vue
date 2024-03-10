<template>
    <div class="chat mt-3">
        <div class="contact">
            <div class="name">Debugging Agent</div>
        </div>
        <div id="chat-messages" class="messages" ref="messages">
            <div v-for="(message, index) in chatMessages" :key="index">
                <div :class="message.role === 'user' ? 'message user' : 'message bot'">
                    <div v-if="message.role === 'assistant' && message.isTyping" class="typing">
                        <div class="dot dot-1"></div>
                        <div class="dot dot-2"></div>
                        <div class="dot dot-3"></div>
                    </div>
                    <div v-else v-html="message.content"></div>
                </div>
            </div>
        </div>
        <div class="input">
            <input type="text" v-model="question" placeholder="Type your question here!" @keyup.enter="sendMessage"  ref="questionInputRef"/>
            <button @click="sendMessage" class="btn btn-primary">Send</button>
        </div>
    </div>
</template>
  
  
<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';


interface ChatMessage {
    content: string;
    role: 'user' | 'assistant';
    isTyping?: boolean;
    dropdownItems?: string[];
}

interface ChatMessageBackend {
    content: string;
    role: 'user' | 'assistant';
}


export default defineComponent({
    data() {
        return {
            question: ref<string>(''),
            feedback: '',
            currentIndex: -1,
            showChatbox: ref(false),
            chatMessages: [] as ChatMessage[], // Define the type for chatMessages
            backendURL: '/api',
            isRecording: ref<boolean>(false),
            isDropdownOpen: ref(false),
            isPinStartClicked: ref(false),
            isPinEndClicked: ref(false),
        };
    },
    methods: {
        async sendMessage() {

            if (this.question.trim() === '') {
                return;
            }

            // Add user message to the chat
            this.chatMessages.push({ content: this.question, role: 'user', isTyping: false });

            // Simulate a bot response with typing animation
            this.chatMessages.push({ content: 'Bot is typing...', role: 'assistant', isTyping: true });


            this.scrollToBottom();


            const requestBody = {
                messages: this.mapChatMessagesToBackendFormat(this.chatMessages.slice(0, -1))
            };

            this.question = '';


            try {
                // Make a POST request to your API
                const response = await axios.post(`${this.backendURL}/feedbacks/conversation`, requestBody);
                this.chatMessages.pop();
                if (response.status === 200) {
                    // Update the feedback field with the response from GPT-4
                    this.scrollToBottom();
                    const repliedMessage = response.data.data;
                    this.chatMessages.push({ content: repliedMessage, role: 'assistant', isTyping: false});
                    if (this.chatMessages.length == 4) {
                        this.chatMessages.push({ content: "Do you want to try saying this part again in a better way? I can give you feedback again based on that", role: 'assistant', isTyping: false });
                    }
                } else {
                    // Handle API response error
                    console.error('Failed to get chat from GPT-4:', response.status, response.data);
                    this.scrollToBottom();
                }
            } catch (error) {
                // Handle network or other errors
                console.error('Error while chatting with GPT-4:', error);
            }


        },

        mapChatMessagesToBackendFormat(chatMessages: ChatMessage[]) {
            const chatMessagesWithoutTyping = chatMessages.map(({ isTyping,  dropdownItems, ...rest }) => rest);
            return chatMessagesWithoutTyping;
        },

        
        async askGPT() {
            this.showChatbox = true;

            // Send initial message with a dropdown when chatbox is shown
            this.chatMessages.push({
                content: "Hi, what can I help you with?",
                role: 'assistant',
                isTyping: false,
            });
            this.chatMessages.push({
                content: `Try asking these questions`,
                role: 'assistant',
                isTyping: false,
                dropdownItems: [
                    'How to improve this part?',
                    'Could you give me example how to answer this using STAR method?',
                    'How is my performance on this part?',
                    'Could you give me example how to answer this better?',
                    'What is good about this part?',
                ] as string[]
            });
        },

        scrollToBottom() {
            const messagesContainer = this.$refs.messages as HTMLElement;
            if (messagesContainer) {
                this.$nextTick(() => {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                });
            }
        },
    },

    watch: {
       
    },
});
</script>
  
<style scoped>
.contact {
    position: relative;
    padding-left: 2rem;
    height: 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.name {
    font-weight: 500;
    margin-bottom: 0.125rem;
}

.chat {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 50%;
    height: 80vh;
    z-index: 2;
    box-sizing: border-box;
    border-radius: 1rem;
    background: white;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}

.messages {
    /* padding: 6rem; */
    background: #F7F7F7;
    /* You can update the background color as needed */
    flex-shrink: 10;  
    overflow-y: auto;
    height: 50rem;
    box-shadow:
        inset 0 2rem 2rem -2rem rgba(0, 0, 0, 0.05),
        inset 0 -2rem 2rem -2rem rgba(0, 0, 0, 0.05);
}

.message {
    box-sizing: border-box;
    padding: 0.5rem 2rem;
    margin: 1rem;
    background: #FFF;
    border-radius: 1.125rem 1.125rem 1.125rem 0;
    min-height: 2.25rem;
    width: fit-content;
    max-width: 66%;
    box-shadow:
        0 0 2rem rgba(0, 0, 0, 0.075),
        0rem 1rem 1rem -1rem rgba(0, 0, 0, 0.1);
}

.message.user {
    margin: 1rem 1rem 1rem auto;
    border-radius: 1.125rem 1.125rem 0 1.125rem;
    background: #333;
    /* You can update the color as needed */
    color: white;
}

.typing {
    display: flex;
    align-items: center;
}

.dot {
    width: 8px;
    height: 8px;
    background-color: #555;
    border-radius: 50%;
    margin: 0 4px;
    animation: bounce 1s infinite;
}

.dot-1 {
    animation-delay: 0s;
}

.dot-2 {
    animation-delay: 0.2s;
}

.dot-3 {
    animation-delay: 0.4s;
}

@keyframes bounce {

    0%,
    80%,
    100% {
        transform: translateY(0);
    }

    40% {
        transform: translateY(-10px);
    }
}

.input {
    box-sizing: border-box;
    flex-basis: 4rem;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 0.5rem 0 1.5rem;
}

i {
    font-size: 1.5rem;
    margin-right: 1rem;
    color: #666;
    /* You can update the color as needed */
    cursor: pointer;
    transition: color 200ms;
}

i:hover {
    color: #333;
    /* You can update the color as needed */
}

input {
    border: none;
    background-image: none;
    background-color: white;
    padding: 0.5rem 1rem;
    margin-right: 1rem;
    border-radius: 1.125rem;
    flex-grow: 2;
    box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
}

input::placeholder {
    color: #999;
    /* You can update the color as needed */
}

.chat {
    opacity: 1;
    transition: opacity 1s;
    /* Adjust the transition duration as needed */
}

.show-chatbox .chat {
    opacity: 0;
}

.recording {
    color: red;
    /* Change the color to red when recording */
    animation: pulse 1s infinite;
    /* Add a pulsating animation */
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }

    100% {
        transform: scale(1);
    }
}

/* Custom styles for the dropdown */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-button {
    background-color: #6c757d;
    color: #fff;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.dropdown-menu {
    display: none;
    position: absolute;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1;
    min-width: 160px;
}

.dropdown-item {
    padding: 8px 12px;
    text-decoration: none;
    display: block;
    color: #333;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.dropdown:hover .dropdown-menu {
    display: block;
}

@keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

/* Apply the animation to the chatbox */
.message {
    animation: fadeIn 0.5s ease-in-out;
}
.input-group {
  display: flex;
  align-items: center;
}

.time-input {
  flex-grow: 1;
  border: none; /* Remove input border */
}

.input-group-btn {
  padding: 0; /* Remove padding */
  
  border: none;
    background-image: none;
    padding: 0.1rem;
    border-radius: 1.125rem;
    box-shadow: 1px 2px 5px 1px rgba(0, 0, 0, 0.3);
}

.pin-button {
  padding: 0.375rem 0.75rem;
  margin-right: -1px;
  border-top-left-radius: 1.125rem;
  border-bottom-left-radius: 1.125rem;
}

.pin-button-clicked {
    background-color: #ffeca2;
}

.pin-button:hover {
  background-color: #e2e6ea; /* Slightly different background on hover/focus for feedback */
}

.pin-icon {
  width: 16px; /* Or any other size */
  height: auto;
}
</style>