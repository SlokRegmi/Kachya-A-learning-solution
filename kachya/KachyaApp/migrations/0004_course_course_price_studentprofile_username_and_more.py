# Generated by Django 4.1.13 on 2024-07-12 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KachyaApp', '0003_course_course_category_course_no_of_assignment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='hired',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assignment_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='course_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KachyaApp.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='schedule',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='StudentEmail',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='StudentPassword',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='Studentname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='assignment_completed',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
