from django.contrib import admin
from .models import Expense, ExpenseShare, Settlement


class ExpenseShareInline(admin.TabularInline):
    model = ExpenseShare
    extra = 0


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'group', 'amount', 'category', 'paid_by', 'date', 'recurrence')
    list_filter = ('category', 'recurrence', 'split_type')
    search_fields = ('description',)
    date_hierarchy = 'date'
    inlines = [ExpenseShareInline]


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('payer', 'receiver', 'amount', 'group', 'status', 'created_at')
    list_filter = ('status',)
