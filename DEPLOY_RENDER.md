# Deploy no Render — passo a passo

## Pré-requisitos
- Conta no [GitHub](https://github.com) (gratuita)
- Conta no [Render](https://render.com) (gratuita)

---

## 1. Subir o projeto no GitHub

Abra o PowerShell na pasta do projeto e rode:

```powershell
git init
git add .
git commit -m "primeiro commit — settl mvp"
```

Crie um repositório no GitHub (https://github.com/new), depois:

```powershell
git remote add origin https://github.com/SEU_USUARIO/settl.git
git branch -M main
git push -u origin main
```

---

## 2. Criar o banco PostgreSQL no Render

1. Acesse https://render.com e faça login
2. Clique em **New → PostgreSQL**
3. Preencha:
   - **Name:** `settl-db`
   - **Region:** Ohio (US East) ou Frankfurt (mais próximo do BR)
   - **Plan:** Free
4. Clique em **Create Database**
5. Aguarde ~1 minuto e copie o valor de **Internal Database URL**

---

## 3. Criar o Web Service

1. Clique em **New → Web Service**
2. Conecte ao repositório GitHub que você criou
3. Preencha:
   - **Name:** `settl`
   - **Region:** mesma do banco
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
   - **Plan:** Free

---

## 4. Configurar variáveis de ambiente

Na aba **Environment** do Web Service, adicione:

| Variável | Valor |
|---|---|
| `SECRET_KEY` | (gere abaixo) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `settl.onrender.com` |
| `DATABASE_URL` | (Cole o Internal Database URL do passo 2) |

### Gerar o SECRET_KEY

No PowerShell, com o venv ativo:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie o resultado e cole em `SECRET_KEY`.

---

## 5. Deploy

Clique em **Save Changes** → o Render vai:
1. Instalar as dependências (`pip install -r requirements.txt`)
2. Rodar as migrations (`python manage.py migrate`)
3. Coletar os static files (`python manage.py collectstatic`)
4. Iniciar o servidor com gunicorn

Aguarde ~3 minutos. O app estará em:
**https://settl.onrender.com**

---

## 6. Criar o superusuário em produção

No Render, vá em **Shell** (aba do Web Service) e rode:

```bash
python manage.py createsuperuser
```

Ou acesse `/admin/` para gerenciar usuários.

---

## Domínio personalizado (opcional)

Em **Settings → Custom Domains**, adicione `settl.app` ou seu domínio.
Configure o DNS apontando para o Render conforme as instruções da tela.

---

## Limitações do plano gratuito do Render

- O app "dorme" após 15 min sem acesso (cold start de ~30s na primeira visita)
- 750h de uso/mês (suficiente para 1 app 24/7)
- Banco PostgreSQL gratuito expira em 90 dias — faça upgrade ou migre os dados antes

Para produção real, o plano Starter do Render custa US$ 7/mês e elimina o cold start.
