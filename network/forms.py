from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johnsmith'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johnsmith@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'johnsmith123!'}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'johnsmith123!'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Smith'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    handle = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@johnsmith'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean_handle(self):
        handle = self.cleaned_data['handle']
        if not handle.startswith('@'):
            raise forms.ValidationError("Handle must start with '@'.")
        return handle
