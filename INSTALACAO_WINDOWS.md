# Instalação no Windows — passo a passo

## Pré-requisitos

- Python 3.11 ou superior instalado
- Verificar: abra o PowerShell e digite `python --version`

---

## 1. Abra o PowerShell na pasta do projeto

Navegue até onde extraiu o zip:

```powershell
cd C:\Users\Duani\Desktop\rachar-mvp
```

## 2. Crie o ambiente virtual

```powershell
python -m venv venv
```

## 3. Ative o ambiente virtual (IMPORTANTE)

No PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

Se aparecer erro de política de execução, rode antes:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois repita o comando de ativação. Quando ativo, o prompt fica assim:
```
(venv) PS C:\Users\Duani\Desktop\rachar-mvp>
```

## 4. Instale as dependências

Com o venv ativo:
```powershell
pip install django Pillow
```

## 5. Rode as migrations

```powershell
python manage.py migrate
```

## 6. Popule com dados de exemplo

```powershell
python manage.py shell < seed.py
```

Saída esperada:
```
Seed concluído!
  Grupo: República da Barra Funda
  Link de convite: /groups/join/...

Usuários:
  admin@rachar.com  /  admin123  (admin)
  joao@teste.com    /  teste123
  maria@teste.com   /  teste123
```

## 7. Suba o servidor

```powershell
python manage.py runserver
```

## 8. Acesse no navegador

http://127.0.0.1:8000

Entre com: `admin@rachar.com` / `admin123`

---

## Problemas comuns

### "python não é reconhecido"
O Python não está no PATH. Soluções:
- Reinstale o Python marcando a opção **"Add Python to PATH"**
- Ou use `py` no lugar de `python`: `py manage.py runserver`

### Erro de política no Activate.ps1
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Porta 8000 ocupada
```powershell
python manage.py runserver 8080
```
Acesse então: http://127.0.0.1:8080

### "No module named django"
O venv não está ativo. Rode:
```powershell
venv\Scripts\Activate.ps1
pip install django Pillow
```
