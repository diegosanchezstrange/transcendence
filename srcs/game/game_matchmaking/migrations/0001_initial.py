# Generated by Django 4.2.8 on 2024-02-17 16:04

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
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerLeftScore', models.IntegerField(default=0)),
                ('playerRightScore', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('WAITING', 'Waiting'), ('IN_PROGRESS', 'In Progress'), ('PAUSED', 'Paused'), ('FINISHED', 'Finished')], default='WAITING', max_length=20)),
                ('disconnection_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('playerLeft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerLeft', to=settings.AUTH_USER_MODEL)),
                ('playerRight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerRight', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game_matchmaking.game')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
