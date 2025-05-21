<script setup>
import { ref } from 'vue'

const props = defineProps({
  comments: Array
})

const newComment = ref('')
const userName = ref('')
const localComments = ref([...props.comments]) // Cópia para manipulação local

// Adicionar um novo comentário
const addComment = () => {
  if (!userName.value.trim() || !newComment.value.trim()) return

  const newCommentObj = {
    id: Date.now().toString(),
    user: userName.value.trim(),
    content: newComment.value.trim(),
    created_at: new Date().toISOString()
  }

  localComments.value.unshift(newCommentObj) // Adiciona no topo
  userName.value = ''
  newComment.value = ''
}

// Remover um comentário
const deleteComment = (id) => {
  localComments.value = localComments.value.filter(comment => comment.id !== id)
}
</script>

<template>
  <div class="comment-section">
    <h2>Comments ({{ localComments.length }})</h2>

    <div v-if="localComments.length === 0" class="no-comments">
      <p>No comments yet. Be the first to comment!</p>
    </div>

    <div v-for="comment in localComments" :key="comment.id" class="comment">
      <div class="comment-header">
        <span class="comment-user">{{ comment.user }}</span>
        <span class="comment-date">{{ new Date(comment.created_at).toLocaleString() }}</span>
      </div>
      <p class="comment-content">{{ comment.content }}</p>
      <button class="delete-btn" @click="deleteComment(comment.id)">🗑️ Delete</button>
    </div>

    <div class="comment-form">
      <h3>Leave a Comment</h3>
      <input v-model="userName" type="text" placeholder="Your name" />
      <textarea v-model="newComment" placeholder="Write your comment..." rows="3"></textarea>
      <button @click="addComment">Post Comment</button>
    </div>
  </div>
</template>

<style scoped>
.comment-section {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Título */
h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
}

/* Estilo quando não há comentários */
.no-comments {
  text-align: center;
  color: #777;
  font-style: italic;
  margin-bottom: 15px;
}

/* Estilo dos comentários */
.comment {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
  border-radius: 5px;
  background: #f9f9f9;
  position: relative;
}

/* Cabeçalho do comentário */
.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.comment-user {
  font-weight: bold;
  color: #007bff;
}

.comment-date {
  font-size: 0.8rem;
}

/* Conteúdo do comentário */
.comment-content {
  font-size: 1rem;
  color: #333;
  margin-bottom: 8px;
}

/* Botão de exclusão */
.delete-btn {
  position: absolute;
  right: 10px;
  bottom: 10px;
  background: #ff4d4d;
  color: white;
  border: none;
  padding: 5px 10px;
  font-size: 0.8rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}

.delete-btn:hover {
  background: #cc0000;
}

/* Formulário de comentário */
.comment-form {
  margin-top: 20px;
  padding: 15px;
  background: #f1f1f1;
  border-radius: 8px;
}

.comment-form h3 {
  margin-bottom: 10px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

button {
  width: 100%;
  background: #007bff;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}

/* Responsividade */
@media (max-width: 600px) {
  .comment {
    font-size: 0.9rem;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .comment-user {
    margin-bottom: 5px;
  }

  .delete-btn {
    font-size: 0.7rem;
    padding: 4px 8px;
  }
}
</style>
