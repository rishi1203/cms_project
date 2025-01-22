from django.contrib import admin
from .models import User, Category, Content
# Register your models here.



@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    list_filter = ('role',)
    search_fields = ('email', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at','category')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'summary')
