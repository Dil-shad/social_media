# Generated by Django 4.2.2 on 2023-06-30 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_profile_id_user_alter_post_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='user_profile',
        ),
    ]