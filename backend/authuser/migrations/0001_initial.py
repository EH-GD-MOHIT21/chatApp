# Generated by Django 3.2.7 on 2021-09-05 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporarystorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('otp', models.IntegerField()),
                ('send_at', models.DateTimeField()),
                ('f_name', models.CharField(max_length=40)),
                ('l_name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('phoneno', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=13)),
                ('reset_pass_token', models.CharField(blank=True, max_length=100, null=True)),
                ('two_factor_auth', models.BooleanField(default=True)),
                ('index', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]