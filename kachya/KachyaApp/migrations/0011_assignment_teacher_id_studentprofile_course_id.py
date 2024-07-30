# Generated by Django 4.1.13 on 2024-07-30 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KachyaApp', '0010_assignment_remarks_assignment_submitted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='teacher_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KachyaApp.teacherprofile'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='course_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KachyaApp.course'),
        ),
    ]
