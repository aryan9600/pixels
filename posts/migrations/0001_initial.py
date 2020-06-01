# Generated by Django 3.0.6 on 2020-06-01 21:46

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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('image', models.ImageField(upload_to='posts/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('liked_by', models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
