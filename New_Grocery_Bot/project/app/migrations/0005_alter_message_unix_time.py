# Generated by Django 4.2.3 on 2023-08-11 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_message_user_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='unix_time',
            field=models.DateTimeField(),
        ),
    ]