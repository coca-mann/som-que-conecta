## Documentação de Validações da App `accounts`

Este documento descreve as validações e funções implementadas na app `accounts`, com foco na segurança, consistência dos dados e controle de acesso dos usuários.

---

### 1. Validação de `username`
**Arquivo:** `validators.py`

- Garante que não exista outro usuário com o mesmo `username`.
- Validador utilizado no serializer `UserRegistrationSerializer`.

```python
def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError("Esse nome de usuário já está em uso.")
```

---

### 2. Validação de `email`
**Arquivo:** `validators.py`

- Impede que dois usuários compartilhem o mesmo e-mail.
- Usado em `UserRegistrationSerializer`.

```python
def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Um usuário com essa conta de e-mail já existe")
```

---

### 3. Validação de `auth_provider` e `sso_id`
**Arquivo:** `validators.py`

- Se o `auth_provider` for `google`, o campo `sso_id` deve ser preenchido.
- Validação feita no método `validate()` do `UserProfileSerializer`.

```python
def validate_auth_provider_sso_id(auth_provider, sso_id):
    if auth_provider == 'google' and not sso_id:
        raise ValidationError("O campo sso_id é obrigatório quando o provedor de autenticação é Google.")
```

---

### 4. Validação de `date_of_birth`
**Arquivo:** `validators.py`

- Impede datas de nascimento futuras.

```python
from datetime import date

def validate_date_of_birth(date_of_birth):
    if date_of_birth and date_of_birth > date.today():
        raise ValidationError("A data de nascimento não pode estar no futuro.")
```

---

### 5. Validação do campo `profile_picture`
**Arquivo:** `validators.py`

- Permite apenas arquivos de imagem.
- Tamanho máximo permitido: 2MB.
- Ignora arquivos já salvos como string (caminho).

```python
def validate_profile_picture(file):
    max_size = 2 * 1024 * 1024  # 2MB

    if hasattr(file, 'content_type'):
        if not file.content_type.startswith("image/"):
            raise ValidationError("O arquivo deve ser uma imagem válida.")
        if file.size > max_size:
            raise ValidationError("A imagem deve ter no máximo 2MB.")
```

---

### 6. Restrição de acesso ao próprio perfil
**Arquivo:** `UserProfileViewSet`

- O endpoint `/profiles/me/` foi criado para permitir que o usuário veja e edite apenas o próprio perfil.
- O `get_object()` sempre retorna o `UserProfile` associado ao `request.user`.

```python
def get_object(self):
    return UserProfile.objects.get(user=self.request.user)
```

---

### 7. Login social com Google via token (SSO)
**Arquivos:** `views_social.py`, `adapters.py`

- View personalizada com `GoogleOAuth2Adapter` que recebe `access_token` do frontend.
- Adapter customizado (`MySocialAccountAdapter`) extrai e armazena:
  - `email`, `sso_id`, `name`, `picture`
  - Define `auth_provider = 'google'`
  - Cria `UserProfile` com tipo padrão se não existir

**Status:** Implementado com sucesso e funcional via `/auth/social/login/`

---

### 8. (Planejado) Moderação de `bio` com IA

- Ideia definida: armazenar a `bio` em uma tabela intermediária (`PendingBioReview`) e realizar a moderação posteriormente usando uma API externa (como Google Gemini).
- A bio só é publicada se for aprovada pela IA.
- Campo `status` informa se a bio está "pendente", "aprovada" ou "reprovada".

**Status:** a ser implementado.

---

### 9. (Planejado) Redefinição de senha por e-mail

- Rota `/auth/password/reset/` já configurada
- O envio de e-mail funcionará assim que o frontend for finalizado
- A URL de confirmação já está registrada como placeholder

**Status:** aguardando implementação no frontend

