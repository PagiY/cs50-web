# Generated by Django 4.1.1 on 2022-09-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_list_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]