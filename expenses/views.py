from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from groups.models import Group, Membership
from .models import Expense, Settlement
from .forms import ExpenseForm, SettlementForm


def _get_group_and_membership(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, is_active=True)
    membership = get_object_or_404(Membership, user=request.user, group=group, is_active=True)
    return group, membership


@login_required
def expense_create(request, group_pk):
    group, membership = _get_group_and_membership(request, group_pk)
    form = ExpenseForm(group, request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.group = group
        expense.created_by = request.user
        expense.save()
        if expense.split_type == 'equal':
            members = [m.user for m in group.memberships.filter(is_active=True)]
            expense.save_equal_shares(members)
        messages.success(request, f'Despesa "{expense.description}" adicionada!')
        return redirect('group_detail', pk=group.pk)
    return render(request, 'expenses/form.html', {
        'form': form, 'group': group, 'title': 'Nova despesa'
    })


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    group, membership = _get_group_and_membership(request, expense.group.pk)
    shares = expense.shares.select_related('user')
    return render(request, 'expenses/detail.html', {
        'expense': expense, 'group': group, 'shares': shares, 'membership': membership
    })


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    group, membership = _get_group_and_membership(request, expense.group.pk)
    can_delete = (expense.created_by == request.user or membership.role == 'admin')
    if not can_delete:
        messages.error(request, 'Você não tem permissão para excluir esta despesa.')
        return redirect('group_detail', pk=group.pk)
    if request.method == 'POST':
        desc = expense.description
        expense.delete()
        messages.success(request, f'Despesa "{desc}" removida.')
        return redirect('group_detail', pk=group.pk)
    return render(request, 'expenses/confirm_delete.html', {'expense': expense, 'group': group})


@login_required
def settlement_create(request, group_pk):
    group, membership = _get_group_and_membership(request, group_pk)
    form = SettlementForm(group, request.user, request.POST or None)
    if form.is_valid():
        settlement = form.save(commit=False)
        settlement.group = group
        settlement.payer = request.user
        settlement.save()
        messages.success(request, 'Acerto registrado! Aguardando confirmação.')
        return redirect('group_detail', pk=group.pk)
    return render(request, 'expenses/settlement_form.html', {
        'form': form, 'group': group
    })


@login_required
def settlement_confirm(request, pk):
    settlement = get_object_or_404(Settlement, pk=pk, receiver=request.user, status='pending')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            settlement.status = 'confirmed'
            settlement.confirmed_at = timezone.now()
            settlement.save()
            messages.success(request, 'Acerto confirmado! Saldo atualizado.')
        elif action == 'dispute':
            settlement.status = 'disputed'
            settlement.save()
            messages.warning(request, 'Acerto marcado como disputado.')
        return redirect('group_detail', pk=settlement.group.pk)
    return render(request, 'expenses/settlement_confirm.html', {'settlement': settlement})


@login_required
def dashboard(request):
    memberships = request.user.memberships.filter(is_active=True).select_related('group')
    pending_settlements = Settlement.objects.filter(
        receiver=request.user, status='pending'
    ).select_related('payer', 'group')
    my_settlements = Settlement.objects.filter(
        payer=request.user, status='pending'
    ).select_related('receiver', 'group')
    recent_expenses = Expense.objects.filter(
        group__memberships__user=request.user,
        group__memberships__is_active=True
    ).select_related('paid_by', 'group').order_by('-created_at')[:10]
    return render(request, 'dashboard.html', {
        'memberships': memberships,
        'pending_settlements': pending_settlements,
        'my_settlements': my_settlements,
        'recent_expenses': recent_expenses,
    })
