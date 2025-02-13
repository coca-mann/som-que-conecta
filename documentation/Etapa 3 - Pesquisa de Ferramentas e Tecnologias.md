**🚀 Etapa 3: Pesquisa de Ferramentas e Tecnologias 🎯**

### **1. Backend ⚙️💻🔒**
- **Framework:** Django
- **API:** Django Rest Framework (DRF) para garantir segurança e escalabilidade.
- **Banco de Dados:** PostgreSQL
- **Armazenamento de Artigos:** JSONB no PostgreSQL para flexibilidade e eficiência na busca.
- **Busca Full-Text:** Implementação com PostgreSQL (pg_trgm e tsvector) para pesquisas eficientes.
- **Autenticação:** JWT (via `djangorestframework-simplejwt`), considerando compatibilidade com Django Admin.
- **Gerenciamento de Conteúdo:** Django CMS
- **Administração:** Uso do Django Admin para controle de usuários e permissões.
- **SSO:** Implementação de Single Sign-On (SSO) com Google.

### **2. Frontend 🌐📱💡**
- **Framework:** Vue.js
- **Modo de Comunicação:** API REST via Django Rest Framework (DRF)
- **Configuração do CORS:** Uso do pacote `django-cors-headers` para permitir comunicação segura entre frontend e backend.
- **Fluxo de Requisições:** Implementação de login e consumo da API utilizando token JWT.

### **3. Infraestrutura e Hospedagem 🏗️☁️🔧**
- **Hospedagem:** Servidor próprio utilizando Proxmox.
- **Disponibilidade Online:** Integração com Cloudflare Tunnel.
- **Deploys:** Manuais durante as primeiras etapas, com possível migração para Docker no futuro.
- **Armazenamento de Arquivos Estáticos e Mídia:** Local, sem uso de serviços em nuvem.
- **Monitoramento de Logs:** Não implementado no momento, foco no desenvolvimento inicial.

### **4. Notificações e Comunicação ✉️📢📬**
- **Envio de E-mails:** Uso inicial de um servidor SMTP gratuito, com migração futura para um SMTP próprio.
- **Tipos de E-mails:** Alguns serão apenas notificações, outros terão finalidade de marketing (definição será feita durante o desenvolvimento dessa parte do projeto).

