from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')  # Bu xatoga sabab bo'lgan qator
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')  # groups maydoni uchun
