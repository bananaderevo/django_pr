# Generated by Django 3.2.5 on 2021-07-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pr', '0003_post_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Is active'),
        ),
    ]
