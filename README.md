# Rachar — Gerenciamento de despesas em grupo

MVP Django para gestão de despesas compartilhadas em repúblicas e grupos de convivência.

## Stack

- Python 3.11+  |  Django 6.x  |  SQLite (dev)  |  HTML/CSS puro (sem JS framework)

## Instalação rápida

```bash
python -m venv venv && source venv/bin/activate
pip install django Pillow
python manage.py migrate
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Estrutura

```
rachar/
├── config/          # settings, urls, wsgi
├── accounts/        # usuários customizados
├── groups/          # grupos e membros
├── expenses/        # despesas, shares e acertos
├── templates/       # HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── accounts/
│   ├── groups/
│   └── expenses/
├── static/css/
└── manage.py
```

## Funcionalidades MVP

- Cadastro/login por e-mail + chave Pix no perfil
- Grupos com link de convite (UUID) — entrar sem aprovação manual
- Papéis: admin e membro
- Despesas: valor, categoria, quem pagou, data, recorrência
- Divisão igualitária automática com arredondamento correto
- Saldo líquido por usuário e simplificação de dívidas (algoritmo greedy)
- Fluxo de acerto: pendente → confirmado/disputado
- Chave Pix do credor exibida direto no "quem paga pra quem"
- Dashboard com alertas de acertos pendentes

## Regras de negócio

| Regra | Status |
|---|---|
| Usuário em múltiplos grupos | ✅ |
| Divisão igualitária com centavos distribuídos | ✅ |
| Simplificação de dívidas (greedy min/max) | ✅ |
| Saldo só muda após confirmação | ✅ |
| Acerto pode ser disputado | ✅ |
| Só criador ou admin exclui despesa | ✅ |
| Pix exibida no fluxo de acerto | ✅ |
| Convite por link sem pré-cadastro | ✅ |

## Usuários de demo (após rodar seed)

| E-mail | Senha |
|---|---|
| admin@rachar.com | admin123 |
| joao@teste.com | teste123 |
| maria@teste.com | teste123 |

## Próximos passos

- Divisão personalizada (valor fixo / percentual por membro)
- Leitura de QR Code de NF-e brasileira
- Integração Pix via Open Finance
- Notificações por e-mail
- Exportação CSV/PDF
- Fundo comum do grupo (caixinha)
