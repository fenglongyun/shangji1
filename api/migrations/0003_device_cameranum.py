# Generated by Django 3.1.1 on 2020-10-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201019_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='cameranum',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='摄像头设备号'),
        ),
    ]