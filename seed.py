"""
Execute com: python manage.py shell < seed.py
Popula o banco com dados de demonstração.
"""
from accounts.models import User
from groups.models import Group, Membership
from expenses.models import Expense
from decimal import Decimal
import datetime

print("Criando usuários...")
u1, _ = User.objects.get_or_create(
    email='admin@rachar.com',
    defaults=dict(username='admin@rachar.com', first_name='Admin', last_name='Teste', pix_key='admin@rachar.com', is_staff=True, is_superuser=True)
)
u1.set_password('admin123'); u1.save()

u2, _ = User.objects.get_or_create(
    email='joao@teste.com',
    defaults=dict(username='joao@teste.com', first_name='João', last_name='Silva', pix_key='joao@teste.com')
)
u2.set_password('teste123'); u2.save()

u3, _ = User.objects.get_or_create(
    email='maria@teste.com',
    defaults=dict(username='maria@teste.com', first_name='Maria', last_name='Souza', pix_key='123.456.789-00')
)
u3.set_password('teste123'); u3.save()

print("Criando grupo...")
g, created = Group.objects.get_or_create(
    name='República da Barra Funda',
    defaults=dict(type='republica', description='Nossa rep do segundo ano', created_by=u1)
)
if created:
    Membership.objects.create(user=u1, group=g, role='admin')
    Membership.objects.create(user=u2, group=g, role='member')
    Membership.objects.create(user=u3, group=g, role='member')

members = [u1, u2, u3]

print("Criando despesas...")
if not g.expenses.exists():
    e1 = Expense.objects.create(
        group=g, description='Aluguel de março', amount=Decimal('2100.00'),
        category='aluguel', paid_by=u1, split_type='equal',
        recurrence='monthly', date=datetime.date(2026, 3, 1), created_by=u1
    )
    e1.save_equal_shares(members)

    e2 = Expense.objects.create(
        group=g, description='Conta de luz', amount=Decimal('180.00'),
        category='energia', paid_by=u2, split_type='equal',
        date=datetime.date(2026, 3, 10), created_by=u2
    )
    e2.save_equal_shares(members)

    e3 = Expense.objects.create(
        group=g, description='Internet fibra', amount=Decimal('99.90'),
        category='internet', paid_by=u3, split_type='equal',
        recurrence='monthly', date=datetime.date(2026, 3, 5), created_by=u3
    )
    e3.save_equal_shares(members)

print(f"\nSeed concluído!")
print(f"  Grupo: {g.name}")
print(f"  Link de convite: /groups/join/{g.invite_token}/")
print(f"\nUsuários:")
print(f"  admin@rachar.com  /  admin123  (admin)")
print(f"  joao@teste.com    /  teste123")
print(f"  maria@teste.com   /  teste123")
