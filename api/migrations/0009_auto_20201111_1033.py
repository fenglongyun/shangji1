# Generated by Django 3.1.1 on 2020-11-11 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20201111_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='level',
            field=models.IntegerField(max_length=1, null=True, verbose_name='菜单级别'),
        ),
    ]
