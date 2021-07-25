from django import forms
from .models import User
from .models import Profile

from .models import Comments
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('short_description', 'description' )


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )
