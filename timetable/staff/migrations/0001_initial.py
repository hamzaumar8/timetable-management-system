# Generated by Django 2.2.5 on 2019-11-02 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("administrator", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("uncompleted", "Uncompleted"),
                            ("pending", "Pending Approval"),
                            ("outgoing", "Outgoing"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="uncompleted",
                        max_length=150,
                    ),
                ),
                (
                    "academic_year",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administrator.AcademicYear",
                    ),
                ),
                ("courses", models.ManyToManyField(to="administrator.Course")),
                (
                    "group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administrator.Group",
                    ),
                ),
                (
                    "lecturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("venues", models.ManyToManyField(to="administrator.Venue")),
            ],
            options={"db_table": "schedule"},
        ),
        migrations.CreateModel(
            name="LectureSchedule",
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
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("day", models.CharField(max_length=50)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "academic_year",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.AcademicYear",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.Course",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.Group",
                    ),
                ),
                (
                    "lecturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "schedule_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.ScheduleTemplate",
                    ),
                ),
                (
                    "venue",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.Venue",
                    ),
                ),
            ],
            options={"db_table": "lecture_schedule"},
        ),
    ]
