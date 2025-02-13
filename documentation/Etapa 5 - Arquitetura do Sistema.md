# **Etapa 5 - Arquitetura do Sistema**

## **📌 Estrutura do Banco de Dados**

## **1️⃣ Tabela `user_types`** (Tipos de Usuário)
Esta tabela armazena os diferentes tipos de usuários do sistema.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único |
| `name`      | `VARCHAR(50)`  | ❌ Não | Nome do tipo de usuário (Ex: "Aluno", "Tutor", "ONG") |
| `description` | `TEXT` (opcional) | ✅ Sim | Descrição detalhada do tipo de usuário |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |

---

## **2️⃣ Tabela `users`** (Usuários)
Tabela que armazena os dados dos usuários do sistema.

| Coluna          | Tipo           | Permite NULL? | Permite Branco? | Descrição |
|----------------|---------------|--------------|----------------|-----------|
| `id`          | `UUID` (PK)    | ❌ Não | - | Identificador único |
| `username`    | `VARCHAR(150)` | ❌ Não | ❌ Não | Nome de usuário (padrão: e-mail para alunos) |
| `email`       | `VARCHAR(255)` | ❌ Não | ❌ Não | E-mail único do usuário |
| `password`    | `HASH` (opcional) | ✅ Sim | ✅ Sim | Senha criptografada (vazio para usuários SSO) |
| `user_type_id` | `UUID (FK -> user_types.id)` | ❌ Não | ❌ Não | Chave estrangeira para `user_types` |
| `date_of_birth` | `DATE` | ✅ Sim | ❌ Não | Data de nascimento (opcional) |
| `bio`         | `TEXT` | ✅ Sim | ✅ Sim | Descrição do usuário |
| `profile_picture` | `VARCHAR(255)` | ✅ Sim | ✅ Sim | URL da imagem de perfil (opcional) |
| `auth_provider` | `ENUM('local', 'google')` | ❌ Não | ❌ Não | Indica se a conta foi criada localmente ou via SSO |
| `sso_id`      | `VARCHAR(255)` | ✅ Sim | ❌ Não | ID único do usuário no provedor SSO (somente se autenticado via SSO) |
| `created_at`  | `TIMESTAMP`    | ❌ Não | - | Data de criação |

---

## **3️⃣ Tabela `instrument_types`** (Tipos de Instrumentos)
Esta tabela armazena os diferentes tipos de instrumentos disponíveis no sistema.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único |
| `name`      | `VARCHAR(100)` | ❌ Não | Nome do instrumento (Ex: Violão, Guitarra, Piano) |
| `description` | `TEXT` (opcional) | ✅ Sim | Descrição do instrumento |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |

---

## **4️⃣ Tabela `user_instruments`** (Instrumentos cadastrados pelos alunos e ONGs)
Esta tabela armazena os instrumentos que os usuários (alunos ou ONGs) adicionam à plataforma.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que cadastrou o instrumento |
| `instrument_type_id` | `UUID (FK -> instrument_types.id)` | ❌ Não | Tipo de instrumento selecionado |
| `color`     | `VARCHAR(50)`  | ✅ Sim | Cor do instrumento (ex: "Marrom", "Preto", "Branco") |
| `brand`     | `VARCHAR(100)` | ✅ Sim | Marca do instrumento (ex: Yamaha, Fender) |
| `description` | `TEXT` (opcional) | ✅ Sim | Descrição personalizada do instrumento |
| `is_available` | `BOOLEAN` | ❌ Não | Indica se o instrumento está disponível para visualização na plataforma (ONGs podem disponibilizar) |
| `location`  | `VARCHAR(255)` | ✅ Sim | Local onde o instrumento está disponível (ONGs) |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |

---

## **5️⃣ Tabela `articles`** (Artigos e Conteúdos Educacionais)
Esta tabela armazena artigos gerais sobre música, aprendizado de instrumentos, técnicas e história musical.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do artigo |
| `title`     | `VARCHAR(255)`  | ❌ Não | Título do artigo |
| `content`   | `JSONB`         | ❌ Não | Corpo do artigo armazenado em JSON |
| `author_id` | `UUID (FK -> users.id)` | ❌ Não | Autor do artigo |
| `tags`      | `VARCHAR[]`     | ✅ Sim | Lista de tags associadas ao artigo |
| `is_published` | `BOOLEAN`    | ❌ Não | Define se o artigo está publicado ou em rascunho |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |
| `updated_at` | `TIMESTAMP`    | ❌ Não | Última modificação |

---

## **6️⃣ Tabela `article_comments`** (Comentários nos Artigos)
Permite que os usuários interajam com os artigos postando comentários.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do comentário |
| `article_id` | `UUID (FK -> articles.id)` | ❌ Não | Artigo ao qual o comentário pertence |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que fez o comentário |
| `content`   | `TEXT`          | ❌ Não | Texto do comentário |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação do comentário |

---

## **7️⃣ Tabela `article_favorites`** (Favoritar Artigos)
Permite que os usuários salvem artigos para acessar depois.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que favoritou o artigo |
| `article_id` | `UUID (FK -> articles.id)` | ❌ Não | Artigo que foi favoritado |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data em que o artigo foi favoritado |
---

## **📌 Estrutura de Aprendizado**

A estrutura de aprendizado foi projetada para oferecer cursos organizados, permitindo que os alunos sigam um fluxo lógico de aprendizado para um instrumento musical específico.

---

## **1️⃣ Tabela `learning_paths`** (Cursos Estruturados)

Essa tabela define os cursos disponíveis para aprendizado de instrumentos musicais.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do curso |
| `name`      | `VARCHAR(255)`  | ❌ Não | Nome do curso (Ex: "Aprendendo Violão do Zero") |
| `description` | `TEXT`         | ✅ Sim | Breve descrição do curso |
| `instrument_type_id` | `UUID (FK -> instrument_types.id)` | ❌ Não | Instrumento ao qual o curso está associado |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |

---

## **2️⃣ Tabela `lessons`** (Lições dentro de um Curso)

Cada **curso (`learning_paths`)** terá várias **lições (`lessons`)** que o aluno precisa completar.

| Coluna         | Tipo            | Permite NULL? | Descrição |
|---------------|----------------|--------------|-----------|
| `id`         | `UUID` (PK)     | ❌ Não | Identificador único |
| `learning_path_id` | `UUID (FK -> learning_paths.id)` | ❌ Não | Curso ao qual essa lição pertence |
| `title`      | `VARCHAR(255)`  | ❌ Não | Nome da lição |
| `content`    | `JSONB`         | ❌ Não | Conteúdo da lição (vídeos, texto, exercícios) |
| `order`      | `INTEGER`       | ❌ Não | Ordem da lição dentro do curso |
| `created_at` | `TIMESTAMP`     | ❌ Não | Data de criação |

---

## **3️⃣ Tabela `user_learning_progress`** (Progresso do Aluno)

Essa tabela registra **o que cada usuário já completou** dentro de um curso.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que está aprendendo |
| `learning_path_id` | `UUID (FK -> learning_paths.id)` | ❌ Não | Curso que o usuário está fazendo |
| `current_lesson_id` | `UUID (FK -> lessons.id)` | ✅ Sim | Última lição completada |
| `completed` | `BOOLEAN`       | ❌ Não | Indica se o curso foi concluído |
| `updated_at` | `TIMESTAMP`    | ❌ Não | Última atualização do progresso |


---
### **4️⃣ Agendamento de Uso dos Instrumentos (`instrument_bookings`)**
Registra quando um usuário deseja utilizar um instrumento.

| Coluna        | Tipo            | Descrição |
|--------------|----------------|-----------|
| `id`        | `UUID` (PK)     | Identificador único |
| `instrument_id` | `UUID (FK -> instruments.id)` | Instrumento agendado |
| `user_id`   | `UUID (FK -> users.id)` | Usuário que agendou |
| `start_time` | `TIMESTAMP`    | Início do uso |
| `end_time`   | `TIMESTAMP`    | Fim do uso |
| `status`    | `ENUM('pendente', 'confirmado', 'cancelado')` | Estado do agendamento |

---

### **5️⃣ Notificações (`notifications`)**
Armazena notificações enviadas aos usuários.

| Coluna        | Tipo            | Descrição |
|--------------|----------------|-----------|
| `id`        | `UUID` (PK)     | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | Usuário destinatário |
| `message`   | `TEXT`          | Conteúdo da notificação |
| `is_read`   | `BOOLEAN`       | Se foi lida ou não |
| `created_at` | `TIMESTAMP`    | Data de envio |

---

### **6️⃣ Comentários e Feedbacks nos Artigos (`comments`)**
Permite interação dos usuários nos artigos publicados.

| Coluna        | Tipo            | Descrição |
|--------------|----------------|-----------|
| `id`        | `UUID` (PK)     | Identificador único |
| `article_id` | `UUID (FK -> articles.id)` | Artigo relacionado |
| `user_id`   | `UUID (FK -> users.id)` | Autor do comentário |
| `content`   | `TEXT`          | Conteúdo do comentário |
| `created_at` | `TIMESTAMP`    | Data de criação |

---

### **7️⃣ Logs de Atividade (`activity_logs`)**
Registro de eventos importantes no sistema para auditoria.

| Coluna        | Tipo            | Descrição |
|--------------|----------------|-----------|
| `id`        | `UUID` (PK)     | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | Usuário que realizou a ação |
| `action`    | `VARCHAR(255)`  | Descrição da ação |
| `timestamp` | `TIMESTAMP`     | Data e hora da ação |

---

## **📌 Próximos Passos**
Agora que temos a estrutura principal definida, podemos:
- **Revisar e otimizar** para garantir que nada importante foi esquecido.
- **Definir relações e integridade** entre as tabelas.
- **Planejar índices e otimizações** para melhorar desempenho.

O que acha desse modelo inicial? Alguma entidade ou detalhe que deveríamos incluir ou modificar? 🚀