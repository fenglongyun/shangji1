# Generated by Django 3.1.1 on 2020-10-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_device_cameranum'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='company',
            field=models.CharField(max_length=50, null=True),
        ),
    ]