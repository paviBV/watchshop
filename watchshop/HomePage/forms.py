from django import forms
from .models import Watches,RatingComment
from django.contrib.auth.forms import AuthenticationForm

class WatchForm(forms.ModelForm):
    class Meta:
        model=Watches
        # fields = ["name",]
        fields = "__all__"
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = "Username", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
class RatingCommentForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i,str(i)) for i in range(6)], label="Rating")
    class Meta:
        model = RatingComment
        fields = ['rating','comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows':4})
            }