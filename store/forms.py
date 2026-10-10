from django import forms
from django.contrib.auth.models import User
from .models import Order


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'postal_code', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': '123 Main St, Apt 4B'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Zip / Postal Code'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
