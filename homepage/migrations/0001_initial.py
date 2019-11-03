# Generated by Django 2.2.5 on 2019-11-03 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'cuisine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('school', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'department',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cuisine', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('borough', models.CharField(blank=True, max_length=100, null=True)),
                ('building', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, max_length=100, null=True)),
                ('longitude', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'restaurant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'school',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('service_type', models.CharField(max_length=100)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('cuisine', models.CharField(max_length=200)),
                ('school', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'userrequest',
                'managed': True,
            },
        ),
    ]
