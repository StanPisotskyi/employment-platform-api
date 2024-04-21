# Generated by Django 5.0.3 on 2024-04-21 10:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_skill_set', to='skill.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'skill')},
            },
        ),
        migrations.CreateModel(
            name='SkillEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_user_set', to=settings.AUTH_USER_MODEL)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_link_set', to='skill.userskill')),
            ],
            options={
                'unique_together': {('link', 'user')},
            },
        ),
    ]
