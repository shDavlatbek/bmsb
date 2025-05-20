from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(GroupAdmin):
    readonly_fields = ('name',)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_school_admin', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'school')
    fieldsets = (
        (None, 
            {"fields": ("username", "password", "school")}
        ),
        # (
        #     _("Personal info"), {"fields": ("first_name", "last_name", "email")}
        # ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    # "user_permissions",
                ),
            },
        ),
        # (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    def save_model(self, request, obj, form, change):
        """
        When saving a new admin user:
        1. Ensure they have is_staff set to True
        2. Add them to the "Maktab Admin" group
        """
        # Ensure the user is marked as staff
        if obj.school is not None:
            obj.is_staff = True
            
        # Save the user first so we can add them to a group
        super().save_model(request, obj, form, change)
        
        # If this is a new school admin user, add them to the Maktab Admin group
        if not change and obj.school is not None:
            # Try to get the Maktab Admin group
            maktab_admin_group, created = Group.objects.get_or_create(name="Maktab Admin")
            
            # Add the user to the group
            obj.groups.add(maktab_admin_group)
    
    def is_school_admin(self, obj):
        """
        Check if a user is a school admin (has is_staff=True and belongs to a school)
        """
        return obj.is_staff and obj.school is not None
    
    is_school_admin.boolean = True
    is_school_admin.short_description = "Maktab admin"
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.pk == request.user.pk:
            return True
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser