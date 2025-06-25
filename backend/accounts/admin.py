from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from backend.accounts.models import User, UserGoals, UserHistory, EmailVerificationToken


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'skill_level', 'is_professor', 'is_ong', 'is_active', 'date_joined')
    list_filter = ('skill_level', 'is_professor', 'is_ong', 'is_active', 'auth_provider', 'gender', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'profile_picture_preview')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'birthday', 'gender', 'bio', 'profile_picture', 'profile_picture_preview')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_professor', 'is_ong', 'groups', 'user_permissions'),
        }),
        ('Configurações de Habilidade', {
            'fields': ('skill_level',)
        }),
        ('Autenticação', {
            'fields': ('auth_provider', 'sso_id')
        }),
        ('Datas Importantes', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.profile_picture.url
            )
        return "Sem foto"
    profile_picture_preview.short_description = 'Preview da Foto'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(UserGoals)
class UserGoalsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'to_do_date', 'created_at', 'is_overdue')
    list_filter = ('to_do_date', 'created_at')
    search_fields = ('title', 'description', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'to_do_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'to_do_date')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        from django.utils import timezone
        if obj.to_do_date < timezone.now().date():
            return format_html('<span style="color: red;">Sim</span>')
        return format_html('<span style="color: green;">Não</span>')
    is_overdue.short_description = 'Vencido'
    is_overdue.boolean = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'object_name', 'object_id', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__email', 'object_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'action', 'object_name', 'object_id')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        # Histórico deve ser criado automaticamente, não manualmente
        return False


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_expired_display')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'is_expired_display')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'is_expired_display'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired_display(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: red;">Expirado</span>')
        return format_html('<span style="color: green;">Válido</span>')
    is_expired_display.short_description = 'Status do Token'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        # Tokens devem ser criados automaticamente, não manualmente
        return False
