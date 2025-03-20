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

## **📌 Estrutura de Instrumentos**

Os instrumentos cadastrados na plataforma podem ser registrados tanto por **alunos** quanto por **ONGs**. Cada instrumento possui um **tipo predefinido**, mas pode ter características individuais, como cor e marca. ONGs podem disponibilizar instrumentos para uso da comunidade.

---

## **3️⃣ Tabela `instrument_types`** (Tipos de Instrumentos)
Esta tabela armazena os diferentes tipos de instrumentos disponíveis no sistema. Esses tipos servem como categorias para os instrumentos cadastrados por usuários.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único do tipo de instrumento |
| `name`      | `VARCHAR(100)` | ❌ Não | Nome do tipo de instrumento (Ex: Violão, Guitarra, Piano) |
| `description` | `TEXT` (opcional) | ✅ Sim | Descrição detalhada sobre o tipo de instrumento |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação do registro |

🔹 **Definições adicionais:**
✅ Os tipos de instrumentos são **fixos** e cadastrados no sistema previamente.  
✅ ONGs e alunos escolhem um tipo ao cadastrar um novo instrumento.  
✅ Permite fácil categorização e pesquisa de instrumentos na plataforma.  

---

## **4️⃣ Tabela `user_instruments`** (Instrumentos cadastrados pelos alunos e ONGs)
Esta tabela armazena os instrumentos que os usuários adicionam à plataforma, permitindo o registro de instrumentos particulares (alunos) e compartilhados (ONGs).

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único do instrumento |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário (aluno ou ONG) que cadastrou o instrumento |
| `instrument_type_id` | `UUID (FK -> instrument_types.id)` | ❌ Não | Tipo de instrumento selecionado |
| `color`     | `VARCHAR(50)`  | ✅ Sim | Cor do instrumento (ex: "Marrom", "Preto", "Branco") |
| `brand`     | `VARCHAR(100)` | ✅ Sim | Marca do instrumento (ex: Yamaha, Fender) |
| `description` | `TEXT` (opcional) | ✅ Sim | Descrição personalizada do instrumento |
| `is_available` | `BOOLEAN` | ❌ Não | Indica se o instrumento está disponível para visualização na plataforma (ONGs podem disponibilizar) |
| `location`  | `VARCHAR(255)` | ✅ Sim | Local onde o instrumento está disponível (ONGs) |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação do registro |

🔹 **Definições adicionais:**
✅ **Alunos** podem adicionar seus próprios instrumentos e editar seus dados.  
✅ **ONGs** podem cadastrar instrumentos para disponibilização pública.  
✅ Instrumentos cadastrados por ONGs podem ser **visíveis na plataforma**, enquanto os de alunos são privados por padrão.  
✅ O campo `is_available` define se um instrumento pode ser exibido publicamente.  
✅ O campo `location` é útil para ONGs que desejam informar onde o instrumento pode ser encontrado.  

Essa estrutura permite um controle eficiente sobre os instrumentos cadastrados na plataforma, garantindo flexibilidade para alunos e ONGs.



---

## **📌 Estrutura de Artigos e Conteúdos Educacionais**

Os artigos e conteúdos educacionais são parte fundamental da plataforma, permitindo que tutores compartilhem conhecimentos sobre música, aprendizado de instrumentos, técnicas e história musical. Além disso, os usuários podem interagir com os artigos por meio de comentários e favoritar conteúdos para acessar posteriormente.

---

## **5️⃣ Tabela `articles`** (Artigos e Conteúdos Educacionais)
Esta tabela armazena artigos gerais sobre música e aprendizado, podendo conter textos, imagens e vídeos dentro de um formato estruturado.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do artigo |
| `title`     | `VARCHAR(255)`  | ❌ Não | Título do artigo |
| `content`   | `JSONB`         | ❌ Não | Corpo do artigo armazenado em JSON (permite formatação estruturada) |
| `author_id` | `UUID (FK -> users.id)` | ❌ Não | Autor do artigo |
| `tags`      | `VARCHAR[]`     | ✅ Sim | Lista de tags associadas ao artigo |
| `is_published` | `BOOLEAN`    | ❌ Não | Define se o artigo está publicado ou em rascunho |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação |
| `updated_at` | `TIMESTAMP`    | ❌ Não | Última modificação |

🔹 **Definições adicionais:**
✅ Os artigos podem conter **formatação avançada** e **mídias** armazenadas no campo `content` como JSON.  
✅ Os artigos podem ser **organizados por tags**, facilitando a busca e categorização.  
✅ Os tutores podem criar artigos como **rascunho** antes da publicação.  

---

## **6️⃣ Tabela `article_comments`** (Comentários nos Artigos)
Os usuários podem interagir com os artigos postando comentários, permitindo maior engajamento na plataforma.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do comentário |
| `article_id` | `UUID (FK -> articles.id)` | ❌ Não | Artigo ao qual o comentário pertence |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que fez o comentário |
| `content`   | `TEXT`          | ❌ Não | Texto do comentário |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação do comentário |

🔹 **Definições adicionais:**
✅ Apenas usuários autenticados podem comentar.  
✅ Os comentários são exibidos **em ordem cronológica** dentro de cada artigo.  
✅ No futuro, podemos adicionar a funcionalidade de **responder a comentários**.  

---

## **7️⃣ Tabela `article_favorites`** (Favoritar Artigos)
Os usuários podem favoritar artigos para acessá-los posteriormente na plataforma.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que favoritou o artigo |
| `article_id` | `UUID (FK -> articles.id)` | ❌ Não | Artigo que foi favoritado |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data em que o artigo foi favoritado |

🔹 **Definições adicionais:**
✅ Os artigos favoritados ficam salvos no perfil do usuário para fácil acesso.  
✅ Um usuário pode favoritar **quantos artigos desejar**.  
✅ O sistema pode sugerir artigos baseados nos favoritos do usuário no futuro.  

---

Essa estrutura garante uma experiência enriquecedora para os usuários, permitindo a criação, organização e interação com conteúdos educacionais.


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

## **📌 Estrutura de Agendamentos de Instrumentos**

O sistema de agendamentos permite que **ONGs disponibilizem instrumentos** e **alunos reservem horários** para utilizá-los.

---

## **1️⃣ Tabela `instrument_availability`** (Disponibilidade dos Instrumentos)

Essa tabela define **os períodos em que um instrumento está disponível para agendamento**.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único |
| `instrument_id` | `UUID (FK -> user_instruments.id)` | ❌ Não | Instrumento disponível para agendamento |
| `available_from` | `TIMESTAMP` | ❌ Não | Data e hora de início da disponibilidade |
| `available_to` | `TIMESTAMP`   | ❌ Não | Data e hora de fim da disponibilidade |
| `recurring`  | `BOOLEAN`      | ❌ Não | Indica se a disponibilidade se repete periodicamente |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de criação do registro |

---

## **2️⃣ Tabela `instrument_bookings`** (Agendamentos de Instrumentos)

Essa tabela armazena **as reservas feitas pelos alunos** para utilizar os instrumentos cadastrados.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único do agendamento |
| `instrument_id` | `UUID (FK -> user_instruments.id)` | ❌ Não | Instrumento agendado |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário que fez o agendamento |
| `start_time` | `TIMESTAMP`    | ❌ Não | Data e hora de início do uso |
| `end_time`   | `TIMESTAMP`    | ❌ Não | Data e hora de fim do uso |
| `status`    | `ENUM('pendente', 'confirmado', 'cancelado')` | ❌ Não | Estado do agendamento |
| `expires_at` | `TIMESTAMP`    | ✅ Sim | Data e hora limite para confirmação do agendamento |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data da criação do agendamento |

---

## **📌 Sistema de Notificações e Cancelamento Automático de Reservas**

Para garantir que os usuários sejam informados sobre ações relevantes e evitar reservas pendentes indefinidamente, o sistema contará com um **módulo de notificações** e um **mecanismo de cancelamento automático de reservas**.

---

## **3️⃣ Tabela `notifications`** (Notificações)

Essa tabela armazenará todas as notificações enviadas aos usuários.

| Coluna        | Tipo            | Permite NULL? | Descrição |
|--------------|----------------|--------------|-----------|
| `id`        | `UUID` (PK)     | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ❌ Não | Usuário destinatário da notificação |
| `message`   | `TEXT`          | ❌ Não | Conteúdo da notificação |
| `type`      | `ENUM('agendamento', 'cancelamento', 'lembrete')` | ❌ Não | Tipo de notificação |
| `is_read`   | `BOOLEAN`       | ❌ Não | Indica se a notificação foi lida |
| `created_at` | `TIMESTAMP`    | ❌ Não | Data de envio |

---

## **4️⃣ Cancelamento Automático de Reservas**

Para evitar que reservas fiquem indefinidamente **pendentes**, o sistema cancelará automaticamente reservas não confirmadas dentro de um período definido.

### **Regras de Cancelamento Automático:**
1. **Tempo máximo de confirmação:**  
   - Se um agendamento permanecer **pendente por mais de 24 horas**, ele será automaticamente **cancelado**.

2. **Notificação antes do cancelamento:**  
   - O sistema enviará uma **notificação** ao usuário alertando sobre a expiração iminente da reserva.

3. **Liberação do horário do instrumento:**  
   - Quando um agendamento for cancelado automaticamente, o **horário volta a ficar disponível** para outros usuários.

### **Como Funciona?**
✅ Quando um agendamento é criado com status `"pendente"`, o campo `expires_at` recebe `created_at + 24h`.  
✅ Um processo automático checa periodicamente se `expires_at < NOW()` e cancela a reserva.  
✅ O usuário recebe uma **notificação** caso seu agendamento seja cancelado.  


---

## **📌 Estrutura de Logs do Sistema**

Os logs permitem monitorar ações importantes realizadas por usuários e pelo sistema, garantindo auditoria, rastreamento e depuração de erros.

---

## **1️⃣ Tabela `activity_logs`** (Registro de Atividades)

Essa tabela registra **ações realizadas por usuários ou pelo sistema**.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único |
| `user_id`   | `UUID (FK -> users.id)` | ✅ Sim | Usuário que realizou a ação (NULL se for um evento automático) |
| `action`    | `VARCHAR(255)`  | ❌ Não | Descrição da ação realizada |
| `entity`    | `VARCHAR(100)`  | ✅ Sim | Tipo de entidade afetada (ex: "agendamento", "artigo", "instrumento") |
| `entity_id` | `UUID` (opcional) | ✅ Sim | ID do item afetado pela ação |
| `details`   | `JSONB`         | ✅ Sim | Informações adicionais sobre a ação (ex: valores antes e depois da edição) |
| `timestamp` | `TIMESTAMP`    | ❌ Não | Data e hora do evento |

---

## **2️⃣ Tabela `system_logs`** (Registro de Eventos do Sistema)

Essa tabela registra **eventos técnicos do sistema**, como erros, avisos e eventos automáticos.

| Coluna        | Tipo           | Permite NULL? | Descrição |
|--------------|---------------|--------------|-----------|
| `id`        | `UUID` (PK)    | ❌ Não | Identificador único |
| `event_type` | `ENUM('info', 'warning', 'error')` | ❌ Não | Tipo do evento (informação, aviso ou erro) |
| `message`   | `TEXT`         | ❌ Não | Mensagem detalhada sobre o evento |
| `context`   | `JSONB`        | ✅ Sim | Informações adicionais sobre o evento (ex: stack trace de um erro) |
| `timestamp` | `TIMESTAMP`    | ❌ Não | Data e hora do evento |

---

## **📌 Regras de Acesso aos Logs**

O acesso aos logs será restrito conforme os **níveis de permissão** dos usuários.

### **1️⃣ Tipos de Logs e Seus Níveis de Acesso**
| Tipo de Log        | Quem Pode Acessar? | Ações Permitidas |
|--------------------|--------------------|------------------|
| **`activity_logs` (Registro de Atividades)** | Administradores, ONGs (somente suas próprias ações) | Visualizar, filtrar |
| **`system_logs` (Registro de Eventos do Sistema)** | Apenas Administradores | Visualizar, filtrar, excluir (se necessário) |

### **2️⃣ Permissões por Tipo de Usuário**
| Tipo de Usuário | Pode Acessar `activity_logs`? | Pode Acessar `system_logs`? | Pode Excluir Logs? |
|---------------|--------------------------------|-----------------------------|---------------------|
| **Administrador** | ✅ Sim (todos os registros) | ✅ Sim | ✅ Sim |
| **ONG** | ✅ Sim (somente suas próprias ações) | ❌ Não | ❌ Não |
| **Tutor** | ❌ Não | ❌ Não | ❌ Não |
| **Aluno** | ❌ Não | ❌ Não | ❌ Não |

### **3️⃣ Regras Gerais**
- **ONGs só veem logs de suas próprias ações** e não podem acessar logs de outras ONGs.  
- **Logs do sistema (`system_logs`) são restritos** a administradores.  
- **Os logs são imutáveis**, ou seja, não podem ser editados.  
- **Exclusão de logs apenas em casos críticos**, e somente por administradores.  

---

Essa estrutura garante segurança, rastreabilidade e permite futura integração com ferramentas de monitoramento caso necessário.


---

## **📌 Próximos Passos**
Agora que temos a estrutura principal definida, podemos:
- **Revisar e otimizar** para garantir que nada importante foi esquecido.
- **Definir relações e integridade** entre as tabelas.
- **Planejar índices e otimizações** para melhorar desempenho.

O que acha desse modelo inicial? Alguma entidade ou detalhe que deveríamos incluir ou modificar? 🚀