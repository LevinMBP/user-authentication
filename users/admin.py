from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.core.exceptions import ValidationError

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "first_name", "last_name", "start_date", "last_login", "is_client", "is_driver", "is_active", "is_staff", "is_admin", "is_superuser", "pk"]
    list_filter = ["email", "is_active", "is_staff", "is_admin"]
    ordering = ["email"]
    fieldsets = [
        (None, {
            "fields": ["email", "password", "last_login"]
        }),
        ("Personal info", {
            "fields": ["first_name", "last_name", "start_date"]
        }),
        ("Permissions", {
            "fields": ["is_client", "is_driver", "is_active", "is_staff", "is_admin", "groups", "user_permissions"]
        }),
    ]
    filter_horizontal = ("groups", "user_permissions")
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email", 
                    "first_name", 
                    "last_name",
                    "department",
                    "password1", 
                    "password2", 
                    "is_client", 
                    "is_driver", 
                    "is_active", 
                    "is_staff"
                ],
            },
        ),
    ]
    search_fields = ["email"]
    
# class UserChangeFormAdmin(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """

#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = MyUser
#         fields = ["first_name", "last_name", "email", "password", "is_active", "is_staff", "is_admin"]

# class UserCreationFormAdmin(forms.ModelForm):
#     # This is the form for creating new users.
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label="Password confirmation", widget=forms.PasswordInput
#     )
#     class Meta:
#         model = MyUser
#         fields = ['first_name', 'last_name', 'email']

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

admin.site.register(MyUser, UserAdmin)