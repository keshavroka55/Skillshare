from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Chat,Rating



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email Address.')

    class Meta:
        model = User
        fields = ('username', 'email','password1','password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image','bio','skills_i_have','skills_i_need','social_account_link','location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'skills_i_have': forms.Textarea(attrs={'rows': 3}),
            'skills_i_need': forms.Textarea(attrs={'rows': 3}),
        }

        # add here for storing the skills in clean and small letter.

class ChartForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control','placeholder':'Type Your Messages....'})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'feedback']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }