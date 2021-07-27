from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comments


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


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    # email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    short_description = forms.CharField(required=False, help_text='Info')
    description = forms.CharField(required=False, help_text='About')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'short_description', 'description')

    # def clean_email(self):
    #     username = self.cleaned_data.get('username')
    #     email = self.cleaned_data.get('email')
    #
    #     if email and User.objects.filter(email=email).exclude(username=username).count():
    #         raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
    #     return email

    def save(self, commit=True):
        user = super(UpdateProfile, self).save(commit=False)

        # user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.short_description = self.cleaned_data['short_description']
        user.description = self.cleaned_data['description']
        user.username = self.cleaned_data['username']


        if commit:
            user.save()

        return user