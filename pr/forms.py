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


# class CommentsForm(forms.ModelForm):
#     class Meta:
#         model = Comments
#         fields = ('text', )


class NameForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('name',)


class FeedbackForm(forms.Form):
    contact_name = forms.CharField(max_length=150)
    contact_email = forms.EmailField(max_length=150)
    content = forms.CharField(
        widget=forms.Textarea
    )