
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


 
class UpdateProfilePic(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
