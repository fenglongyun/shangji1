# Generated by Django 3.1.1 on 2020-11-07 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_group_group_permissions_permission_user_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group_permissions',
            name='group',
        ),
        migrations.RemoveField(
            model_name='group_permissions',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='user_groups',
            name='group',
        ),
        migrations.RemoveField(
            model_name='user_groups',
            name='userinfo',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Group_permissions',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='User_groups',
        ),
    ]
