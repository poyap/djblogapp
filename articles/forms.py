
from django.forms import widgets
from .models import Article,Profile,Comment
from django.contrib.auth.models import User 
from django import forms
from django.contrib.auth.forms import UserCreationForm 


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model  = Article
        fields = '__all__'
        exclude = ['user','likes']

        widgets = {
            'content':forms.Textarea(attrs={'placeholder':'You can use markdown syntax here'})
        }
class UserRegistrationform(UserCreationForm):
    email = forms.EmailField()
    # first_name = forms.CharField(max_length=100)
    # last_name = forms.CharField(max_length=100)
    # profile_image     = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username','email']


    # i used crispy form tags so i don't need this anymore.
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['email'].widget.attrs['class'] = 'form-control'
 
            # this was a way of adding some widgets to html tags rendered,but i think since we inheritted User class it did't work.
    # widgets = {
    #     'username' : forms.TextInput(attrs={'class':'form-control'}),
    #     'first_name' : forms.TextInput(attrs={'class':'form-control'}),
    #     'last_name' : forms.TextInput(attrs={'class':'form-control'}),
    #     'email' : forms.EmailInput(attrs={'class':'form-control'}),
    # }
    
    #this was totally worked.
    
    # def clean_pass_validation(self):
    #     if self.cleaned_data['new_password'] == self.cleaned_data['confirm_password']:
    #         return self.cleaned_data['confirm_password']
    #     else:
    #         raise forms.ValidationError('passwords don\'t match')

class UpdateProfilePic(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']