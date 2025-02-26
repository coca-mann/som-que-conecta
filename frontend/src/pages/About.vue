<template>
  <div class="container">
    <h1>About "Som que Conecta" 🎶</h1>
    <p class="intro">
      "Som que Conecta" é um projeto dedicado a democratizar o acesso à educação musical,
      promovendo inclusão social através de tecnologia e colaboração.
    </p>

    <!-- Seção Missão -->
    <div class="section">
      <h2>🎯 Nossa Missão</h2>
      <p>
        Nosso objetivo é oferecer materiais educativos, criar um mural de instrumentos disponíveis
        e destacar os benefícios da música na vida das pessoas. Acreditamos que todos merecem a
        oportunidade de aprender e se conectar através da música.
      </p>
    </div>

    <!-- Seção Como Funciona -->
    <div class="section">
      <h2>📌 Como Funciona?</h2>
      <ul>
        <li><strong>📚 Conteúdo Educativo:</strong> Acesse artigos, tutoriais e materiais sobre música.</li>
        <li><strong>🎸 Mural de Instrumentos:</strong> Encontre e disponibilize instrumentos para empréstimo.</li>
        <li><strong>💡 Impacto da Música:</strong> Descubra os benefícios da música na saúde e aprendizado.</li>
      </ul>
    </div>

    <!-- Seção Como Contribuir -->
    <div class="section">
      <h2>🤝 Como Contribuir?</h2>
      <p>
        Se você deseja apoiar o projeto, há diversas maneiras de contribuir:
      </p>
      <ul>
        <li>📤 Doe um instrumento que não usa mais.</li>
        <li>📝 Compartilhe seu conhecimento escrevendo artigos.</li>
        <li>📢 Divulgue o projeto para alcançar mais pessoas.</li>
      </ul>
    </div>

    <!-- Seção Contato e GitHub -->
    <div class="contact-section">
      <h2>📩 Entre em Contato</h2>
      <p>Tem dúvidas, sugestões ou quer colaborar? Entre em contato conosco!</p>
      <a href="mailto:contato@somqueconecta.com" class="contact-button">Enviar E-mail</a>
      
      <h2>💻 Contribua no GitHub</h2>
      <p>Confira o código-fonte e contribua para o desenvolvimento do projeto!</p>
      <a href="https://github.com/coca-mann/som-que-conecta" target="_blank" class="github-button">
        🌍 Acesse o Repositório
      </a>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin-bottom: 15px;
}

.intro {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 30px;
}

.section {
  background: #f9f9f9;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

p, li {
  font-size: 1.1rem;
  color: #444;
  line-height: 1.6;
}

ul {
  list-style: none;
  padding-left: 0;
}

ul li {
  padding: 5px 0;
  display: flex;
  align-items: center;
}

ul li strong {
  margin-right: 5px;
}

/* Seção de contato */
.contact-section {
  text-align: center;
  padding: 20px;
  background: #007bff;
  color: white;
  border-radius: 8px;
}

.contact-section p {
  font-size: 1.2rem;
}

.contact-button, .github-button {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 20px;
  background: white;
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
  border-radius: 5px;
  transition: background 0.2s;
}

.contact-button:hover, .github-button:hover {
  background: #f1f1f1;
}

.github-button {
  display: block;
  margin-top: 15px;
  background: #333;
  color: white;
}

.github-button:hover {
  background: #555;
}
</style>
