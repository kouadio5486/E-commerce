from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"))

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
