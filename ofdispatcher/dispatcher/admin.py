from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from dispatcher.models import Department, DepartmentManager, AlarmLoop, Contact


class DepartmentManagerInline(admin.StackedInline):
    model = DepartmentManager
    can_delete = False
    verbose_name_plural = 'departmentmanagers'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (DepartmentManagerInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Department)
admin.site.register(AlarmLoop)
admin.site.register(Contact)
