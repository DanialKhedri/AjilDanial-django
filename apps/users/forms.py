from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

# فرم ثبت‌نام
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['phone_number']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("رمزها یکسان نیستند")

        if len(p1) < 8 or len(p1) > 50:
            raise forms.ValidationError("رمز باید بین ۸ تا ۵۰ کاراکتر باشد")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# فرم ورود
class LoginForm(forms.Form):
    phone_number = forms.CharField(label='شماره موبایل')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)

    def clean(self):
        phone = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        user = authenticate(phone_number=phone, password=password)
        if not user:
            raise forms.ValidationError("شماره یا رمز اشتباه است")
        self.user = user
        return self.cleaned_data
