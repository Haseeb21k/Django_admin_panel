from django import forms
from .models import Post, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'website', 'location', 'birth_date', 'phone', 
                 'twitter', 'facebook', 'instagram', 'linkedin', 'github']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 234 567 8900'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'https://facebook.com/username'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'https://instagram.com/username'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PostForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        help_text="Select multiple images for this post"
    )
    files = MultipleFileField(
        required=False, 
        help_text="Select multiple files to attach to this post"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({
            'accept': 'image/*',
            'class': 'form-control'
        })
        self.fields['files'].widget.attrs.update({
            'class': 'form-control'
        })