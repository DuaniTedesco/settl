from django.contrib import admin
from .models import Group, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    fields = ('user', 'role', 'is_active', 'joined_at')
    readonly_fields = ('joined_at',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_by', 'is_active', 'created_at')
    list_filter = ('type', 'is_active')
    search_fields = ('name',)
    inlines = [MembershipInline]
    readonly_fields = ('invite_token',)
