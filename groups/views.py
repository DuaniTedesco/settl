import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, Membership
from .forms import GroupForm

UUID_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE)


def _compute_balances(group):
    from expenses.models import Expense, ExpenseShare, Settlement
    from collections import defaultdict
    from decimal import Decimal

    net = defaultdict(Decimal)

    for expense in group.expenses.prefetch_related('shares__user'):
        net[expense.paid_by] += expense.amount
        for share in expense.shares.all():
            net[share.user] -= share.amount

    for settlement in Settlement.objects.filter(group=group, status='confirmed'):
        net[settlement.payer] += settlement.amount
        net[settlement.receiver] -= settlement.amount

    creditors = sorted([(u, v) for u, v in net.items() if v > 0], key=lambda x: -x[1])
    debtors   = sorted([(u, v) for u, v in net.items() if v < 0], key=lambda x:  x[1])
    creditors, debtors = list(creditors), list(debtors)

    transactions = []
    ci = di = 0
    while ci < len(creditors) and di < len(debtors):
        cuser, camount = creditors[ci]
        duser, damount = debtors[di]
        amount = min(camount, -damount)
        transactions.append({'from': duser, 'to': cuser, 'amount': amount})
        creditors[ci] = (cuser, camount - amount)
        debtors[di]   = (duser, damount + amount)
        if creditors[ci][1] == 0:
            ci += 1
        if debtors[di][1] == 0:
            di += 1

    return {'net': dict(net), 'transactions': transactions}


@login_required
def group_list(request):
    memberships = request.user.memberships.filter(is_active=True).select_related('group')
    return render(request, 'groups/list.html', {'memberships': memberships})


@login_required
def group_create(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        group = form.save(commit=False)
        group.created_by = request.user
        group.save()
        Membership.objects.create(user=request.user, group=group, role='admin')
        messages.success(request, f'Grupo "{group.name}" criado!')
        return redirect('group_detail', pk=group.pk)
    return render(request, 'groups/form.html', {'form': form, 'title': 'Novo grupo'})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    membership = get_object_or_404(Membership, user=request.user, group=group, is_active=True)
    members = group.memberships.filter(is_active=True).select_related('user')
    expenses = group.expenses.order_by('-date', '-created_at')[:20]
    balances = _compute_balances(group)
    invite_link = group.get_invite_link(request)
    return render(request, 'groups/detail.html', {
        'group': group,
        'membership': membership,
        'members': members,
        'expenses': expenses,
        'balances': balances,
        'invite_link': invite_link,
    })


@login_required
def group_join(request, token):
    group = get_object_or_404(Group, invite_token=token, is_active=True)
    existing = Membership.objects.filter(user=request.user, group=group).first()
    if existing:
        if existing.is_active:
            messages.info(request, f'Você já é membro de "{group.name}".')
        else:
            existing.is_active = True
            existing.save()
            messages.success(request, f'Bem-vindo de volta a "{group.name}"!')
    else:
        Membership.objects.create(user=request.user, group=group, role='member')
        messages.success(request, f'Você entrou em "{group.name}"!')
    return redirect('group_detail', pk=group.pk)


@login_required
def group_leave(request, pk):
    group = get_object_or_404(Group, pk=pk)
    membership = get_object_or_404(Membership, user=request.user, group=group, is_active=True)
    if request.method == 'POST':
        membership.is_active = False
        membership.save()
        messages.success(request, f'Você saiu de "{group.name}".')
        return redirect('group_list')
    return render(request, 'groups/confirm_leave.html', {'group': group})


@login_required
def group_enter(request):
    error = None
    invite_input = ''

    if request.method == 'POST':
        invite_input = request.POST.get('invite_input', '').strip()
        match = UUID_RE.search(invite_input)

        if not match:
            error = 'Link inválido. Verifique se copiou o link completo e tente novamente.'
        else:
            token = match.group(0)
            group = Group.objects.filter(invite_token=token, is_active=True).first()

            if not group:
                error = 'Convite não encontrado ou expirado. Peça um novo link ao administrador.'
            else:
                existing = Membership.objects.filter(user=request.user, group=group).first()
                if existing:
                    if existing.is_active:
                        messages.info(request, f'Você já é membro de "{group.name}".')
                    else:
                        existing.is_active = True
                        existing.save()
                        messages.success(request, f'Bem-vindo de volta a "{group.name}"!')
                else:
                    Membership.objects.create(user=request.user, group=group, role='member')
                    messages.success(request, f'Você entrou em "{group.name}"! 🎉')
                return redirect('group_detail', pk=group.pk)

    return render(request, 'groups/enter.html', {
        'error': error,
        'invite_input': invite_input,
    })


@login_required
def group_dashboard(request, pk):
    import json
    group = get_object_or_404(Group, pk=pk)
    get_object_or_404(Membership, user=request.user, group=group, is_active=True)
    members = group.memberships.filter(is_active=True).select_related('user')

    expenses = group.expenses.select_related('paid_by').order_by('date')
    expenses_data = []
    for e in expenses:
        month = e.date.strftime('%Y-%m')
        expenses_data.append({
            'month': month,
            'cat': e.category,
            'amount': str(e.amount),
            'payer_id': e.paid_by.pk,
            'payer_name': e.paid_by.get_full_name(),
        })

    return render(request, 'groups/dashboard.html', {
        'group': group,
        'members': members,
        'expenses_json': json.dumps(expenses_data),
    })
