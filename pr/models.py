from django.db import models
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_save


class User(models.Model):
    name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=100)
    description = models.TextField()
    join_date = models.DateField(auto_now=True)

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# class Comments(models.Model):
#     text = models.CharField(max_length=150, null=True)
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         ordering = ['id']
#         verbose_name = 'Comment'
#
#     def __str__(self):
#         return self.text


class Comments(models.Model):
    name = models.CharField(max_length=100)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'comment'

    def __str__(self):
        return self.name


class Post(models.Model):
    text = models.TextField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comments, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'Post: {self.text}'

    def display_comments(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([comments.name for comments in self.comments.all()[:3]])

    def display_all_comments(self):

        return ', '.join([comments.name for comments in self.comments.all()])

    display_comments.short_description = 'Comments'


