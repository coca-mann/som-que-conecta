**Levantamento de Requisitos - Som que Conecta: Música ao Alcance de Todos** 🎵🎶🎼

## 1. Usuários e Perfis 🎭📌📝
### 1.1 Perfis de Usuários
- **Visitantes**: Acessam conteúdo educativo e informações sobre os benefícios da música.
- **Usuários Cadastrados**: Podem interagir com a plataforma, comentar e salvar conteúdos.
- **Professores/Mentores**: Podem adicionar conteúdo educativo e sugerir melhorias.
- **ONGs e Centros Comunitários**: Podem cadastrar e gerenciar instrumentos disponíveis no mural.
- **Administradores**: Gerenciam toda a plataforma, revisam conteúdo e moderam interações.

### 1.2 Níveis de Acesso 🛡️🔑🚪
- **Leitura**: Visitantes podem visualizar conteúdo sem interagir.
- **Interação**: Usuários cadastrados podem comentar, curtir e salvar conteúdos.
- **Gerenciamento**: ONGs e professores podem adicionar recursos.
- **Administração Completa**: Apenas administradores podem moderar e gerenciar o sistema.

---

## 2. Funcionalidades Principais 🚀✨🎯
### 2.1 Conteúdo Educativo 📚🎼🎤
- Antes de acessar os artigos e tutoriais passo a passo sobre aprendizado musical, os usuários preencherão um formulário inicial perguntando qual instrumento lhes interessa, se já possuem o instrumento e se desejam aprender mais sobre música.
- Portfólio de instrumentos com descrições, imagens e história.
- Seção de perguntas frequentes e dicas de aprendizado.

### 2.2 Mural de Instrumentos 🎻🎺🎹
- Cadastro de instrumentos por ONGs e centros comunitários.
- Disponibilidade de instrumentos: Usuários solicitantes podem visualizar os equipamentos disponíveis e solicitar sua utilização. O proprietário do equipamento recebe a requisição e decide sobre a disponibilidade, reduzindo a necessidade de manutenção constante dos status pelos proprietários e ONGs.
- Sistema de localização para encontrar instrumentos por região.
- Possibilidade de contato entre usuários e ONGs.

### 2.3 Benefícios da Música 💙🧠🎶
- Publicação de artigos científicos e estudos sobre os impactos da música na saúde e cognição.
- Depoimentos e histórias de sucesso.
- Eventos e workshops online sobre música e bem-estar.

---

## 3. Requisitos Técnicos 🖥️⚙️📡
### 3.1 Tipo de Plataforma 📱💻🖥️
- Plataforma web responsiva com suporte a tecnologia PWA futuramente, sem versão mobile dedicada.

### 3.2 Tecnologias Propostas 💻🔧🔌
- **Frontend**: Flet (Python) para facilitar o aprendizado e entendimento.
- **Backend**: Django (Python).
- **Banco de Dados**: PostgreSQL.
- **Autenticação**: Login por email/senha e OAuth (Google, Facebook).

### 3.3 Integrações Necessárias 🌍🔗📍
- Google Maps API para localização das ONGs.
- Firebase ou AWS para armazenamento de imagens e arquivos.

---

## 4. Requisitos Não Funcionais 🔐⚡📊
- **Segurança**: Proteção de dados, controle de acesso, criptografia de senhas.
- **Performance**: Otimização para carregamento rápido.
- **Escalabilidade**: Suporte a um grande número de usuários simultaneamente.
- **Acessibilidade**: Compatibilidade com leitores de tela e navegação simplificada.

---

## 5. Fluxo de Uso 🔄📌📊
### 5.1 Acesso e Navegação 🏡🖥️🎶
1. Visitantes acessam a plataforma e exploram conteúdo educativo.
2. Usuários podem se cadastrar para interagir e salvar conteúdo.
3. ONGs e centros comunitários fazem login para cadastrar instrumentos.

### 5.2 Cadastro de Instrumentos 📝🎸✅
1. ONG acessa painel e insere dados do instrumento.
2. Instrumento é disponibilizado no mural.
3. Interessados entram em contato através do sistema.

Esse documento serve como base para ajustes e refinamentos conforme necessário. ✍️📑🛠️

