# Generated by Django 4.0.3 on 2022-03-15 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_rename_bloguser_upvoter_rename_upvoter_upvoter_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upvoter',
            old_name='username',
            new_name='voter_username',
        ),
    ]
