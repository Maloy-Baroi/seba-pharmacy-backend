from django.contrib import admin
from App_login.models import CustomUser


# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff')


admin.site.register(CustomUser, UserModelAdmin)
