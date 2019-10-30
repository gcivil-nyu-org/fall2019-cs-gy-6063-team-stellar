# Generated by Django 2.2.6 on 2019-10-30 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cuisine",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"db_table": "cuisine", "managed": False, },
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("school", models.IntegerField(blank=True, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"db_table": "department", "managed": False, },
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("cuisine",  models.CharField(blank=True, max_length=100, null=True)),
                ("score",  models.IntegerField(blank=True, null=True)),
                ("borough",  models.CharField(blank=True, max_length=100, null=True)),
                ("building",  models.CharField(blank=True, max_length=100, null=True)),
                ("street",  models.CharField(blank=True, max_length=100, null=True)),
                ("zipcode",  models.CharField(blank=True, max_length=100, null=True)),
                ("phone",  models.CharField(blank=True, max_length=100, null=True)),
                ("latitude",  models.CharField(blank=True, max_length=100, null=True)),
                ("longitude",  models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"db_table": "restaurant", "managed": False, },
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"db_table": "school", "managed": False, },
        ),
        migrations.CreateModel(
            name="ServiceType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"db_table": "service_type", "managed": False, },
        ),
    ]
