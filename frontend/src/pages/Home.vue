<template>
  <div class="home-container">
    <!-- Seção Hero -->
    <section class="hero">
      <div class="hero-content">
        <h1>🎶 Conecte-se com a Música</h1>
        <p>Aprenda, compartilhe e explore a música como nunca antes. Junte-se à nossa comunidade!</p>
        <div class="hero-buttons">
          <router-link to="/register" class="cta-button">Comece Agora</router-link>
          <router-link to="/about" class="secondary-button">Saiba Mais</router-link>
        </div>
      </div>
    </section>

    <!-- Seção de Recursos -->
    <section class="features">
      <h2>🌟 O que você encontra aqui?</h2>
      <div class="features-grid">
        <div class="feature-item">
          <img src="https://source.unsplash.com/200x150/?music,education" alt="Educação Musical" />
          <h3>📚 Conteúdo Educativo</h3>
          <p>Tutoriais e artigos para aprender sobre instrumentos e teoria musical.</p>
        </div>
        <div class="feature-item">
          <img src="https://source.unsplash.com/200x150/?guitar,piano" alt="Instrumentos" />
          <h3>🎸 Mural de Instrumentos</h3>
          <p>Encontre e compartilhe instrumentos musicais disponíveis para a comunidade.</p>
        </div>
        <div class="feature-item">
          <img src="https://source.unsplash.com/200x150/?people,concert" alt="Comunidade Musical" />
          <h3>💬 Comunidade Musical</h3>
          <p>Interaja com outros músicos, compartilhe experiências e aprenda juntos.</p>
        </div>
      </div>
    </section>

    <!-- Seção de Depoimentos -->
    <section class="testimonials">
      <h2>💬 O que dizem sobre nós?</h2>
      <div class="testimonial-card">
        <p>"Esse projeto transformou minha forma de aprender música. Nunca foi tão fácil!"</p>
        <span>🎸 João Silva</span>
      </div>
      <div class="testimonial-card">
        <p>"Agora posso compartilhar meu violão com quem quer aprender. Sensacional!"</p>
        <span>🎶 Maria Souza</span>
      </div>
    </section>

    <!-- Chamada para Ação Final -->
    <section class="cta">
      <h2>Pronto para se conectar com a música?</h2>
      <router-link to="/register" class="cta-button">Cadastre-se Agora</router-link>
    </section>
  </div>
</template>

<style scoped>
/* Container principal */
.home-container {
  text-align: center;
}

/* Seção Hero */
.hero {
  background: url("https://source.unsplash.com/1600x600/?music,concert") center/cover;
  color: black;
  padding: 60px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-content {
  max-width: 600px;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.cta-button {
  background: #ff9800;
  color: white;
  padding: 12px 20px;
  font-size: 1.1rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.2s;
}

.cta-button:hover {
  background: #e68900;
}

.secondary-button {
  background: white;
  color: #007bff;
  padding: 12px 20px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  border: 2px solid #007bff;
  transition: background 0.2s;
}

.secondary-button:hover {
  background: #007bff;
  color: white;
}

/* Seção de Recursos */
.features {
  padding: 50px 20px;
  background: #f9f9f9;
}

.features h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.features-grid {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.feature-item {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 250px;
}

.feature-item img {
  width: 100%;
  border-radius: 8px;
}

.feature-item h3 {
  margin: 15px 0 10px;
  font-size: 1.3rem;
}

/* Seção de Depoimentos */
.testimonials {
  padding: 50px 20px;
  background: #007bff;
  color: white;
}

.testimonials h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.testimonial-card {
  background: white;
  color: #333;
  padding: 20px;
  border-radius: 10px;
  margin: 10px auto;
  width: 80%;
  max-width: 500px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
}

.testimonial-card p {
  font-size: 1.2rem;
  font-style: italic;
}

.testimonial-card span {
  display: block;
  margin-top: 10px;
  font-weight: bold;
  font-size: 1rem;
}

/* Chamada para Ação Final */
.cta {
  padding: 50px 20px;
  background: #ff9800;
  color: white;
}

.cta h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

</style>
