# Generated by Django 5.0 on 2023-12-30 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='PieceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='images/')),
                ('brand', models.CharField()),
                ('material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.material')),
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.piecetype')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField()),
                ('name', models.CharField()),
                ('subscription_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.subscriptionlevel')),
            ],
        ),
        migrations.CreateModel(
            name='OutfitPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated', models.BooleanField()),
                ('items', models.ManyToManyField(to='API.item')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.user')),
            ],
        ),
    ]
