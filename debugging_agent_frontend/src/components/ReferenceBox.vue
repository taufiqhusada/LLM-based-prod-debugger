<template>
    <section  v-if="showBox && docs"  ref="chatArea" class="chat-area">
        <div v-for="(doc, index) in docs" :key="index" class="message message-in content-formatter">
            <div class="message-container">
            <div class="content">
                <pre>{{ JSON.parse(doc) }}</pre>
            </div>
            </div>
        </div>
    </section>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    props: {
        docs: {
            type: Array<string>,
        },
        showBox: {
            type: Boolean,
            default: false,
        }
    }
});
</script>

<style scoped>
.headline {
  text-align: center;
}

.chat-area {
  border: 1px solid #ccc;
  background: white;
  max-height: 77vh;
  padding: 1em;
  overflow: auto;
  max-width: 40rem;
  margin: 0 auto 2em auto;
  box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1em;
  margin-bottom: 1em;

  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  max-width: 40rem;
  z-index: 2;
  box-sizing: border-box;
  border-radius: 1rem;
}

.message {
  width: 95%;
  border-radius: 10px;
  padding: .5em;
  margin-bottom: .5em;
  margin-top: .5em;
  font-size: .9em;
  text-align: left;
}

.message-in {
  background: #F1F0F0;
  color: black;
}

.highlight {
  background: #ffeca2;
  /* Highlight color */
  /* Add other styles for highlighting */
}

.highlight-seek-time {
  --tw-text-opacity: 1;
  background: rgb(250, 200, 200);
  /* background: var(--tw-bg-opacity, rgba(255, 236, 162, var(--tw-bg-opacity, 1))); Background color from .highlight */
  /* Highlight color */
  /* Add other
   styles for highlighting */
}


.message-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.time {
  text-align: right;
  margin-right: 10px; /* Adjust margin as needed */
}

.content {
  flex-grow: 1;
}

.content-formatter {
    overflow-x: auto; /* or overflow-x: scroll; */
  white-space: nowrap; 
}


</style>