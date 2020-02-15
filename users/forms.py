from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class LoginForm(forms.Form):
    phone = forms.CharField(label = 'Your Phone Number')
    password = forms.CharField(widget = forms.PasswordInput)

    # def clean(self, *args, **kwargs):
    #     query = self.cleaned_data.get("query")
    #     password = self.cleaned_data.get("password")
    #     user_qs_final = User.objects.filter(
    #             Q(username__iexact=query)|
    #             Q(email__iexact=query)
    #         ).distinct()
    #     if not user_qs_final.exists() and user_qs_final.count() != 1:
    #         raise forms.ValidationError("Invalid credentials -- user not exist")
    #     user_obj = user_qs_final.first()
    #     if not user_obj.check_password(password):
    #             # log auth tries
    #             raise forms.ValidationError("Invalid credentials -- passowrd invalid")
    #     if not user_obj.is_active:
    #                 raise forms.ValidationError("Inactive user. Please verify your email address.")
    #     self.cleaned_data["user_obj"] = user_obj
    #     return super(UserLoginForm, self).clean(*args, **kwargs)


class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Please Enter OTP here')
    

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        # Check that the two password entries match
        phone = self.cleaned_data.get("phone")
        qs = User.objects.filter(phone=phone)

        if qs.exists():
            raise forms.ValidationError("phone is taken")
        return phone

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     user.is_active = False # send confirmation email via signals
    #     # obj = EmailActivation.objects.create(user=user)
    #     # obj.send_activation_email()
    #     if commit:
    #         user.save()
    #     return user


class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()


class SetPasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        #user.is_active = False
        # create a new user hash for activating email.

        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]