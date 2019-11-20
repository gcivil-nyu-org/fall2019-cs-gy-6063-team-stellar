# Generated by Django 2.2.6 on 2019-11-20 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import homepage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_account', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Days',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=8)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cuisine', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('borough', models.CharField(blank=True, max_length=100, null=True)),
                ('building', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Days_left',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('days', models.IntegerField()),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserRequestMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_time', models.DateTimeField(default=homepage.models.in_one_day)),
                ('restaurants', models.ManyToManyField(blank=True, to='homepage.Restaurant')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userrequestmatch_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userrequestmatch_user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('service_type', models.CharField(max_length=100)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('service_status', models.BooleanField(default=True)),
                ('match_status', models.BooleanField(default=False)),
                ('cuisines_priority', models.IntegerField(default=10)),
                ('department_priority', models.IntegerField(default=10)),
                ('interests_priority', models.IntegerField(default=10)),
                ('available_date', models.DateField()),
                ('cuisines', models.ManyToManyField(blank=True, to='homepage.Cuisine')),
                ('days', models.ManyToManyField(to='homepage.Days')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Department')),
                ('interests', models.ManyToManyField(blank=True, to='homepage.Interests')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.School')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=200)),
                ('choices', models.ManyToManyField(blank=True, to='homepage.Choice')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserRequestMatch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_user1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Question'),
        ),
    ]
