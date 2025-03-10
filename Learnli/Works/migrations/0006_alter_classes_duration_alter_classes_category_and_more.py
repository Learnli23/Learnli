# Generated by Django 5.1.1 on 2025-01-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Works', '0005_classes_is_hiden_classes_reported_lessons_is_hiden_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='Duration',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='classes',
            name='category',
            field=models.CharField(choices=[('science', 'science'), ('Arts', 'Arts'), ('Engineering', 'Engineering'), ('Business', 'Business'), ('creative_work', 'creative_work'), ('Languages', 'Languages'), ('computor_science', 'computer_science'), ('others', 'others'), ('Religios_studies', 'Religious_studies')], max_length=200),
        ),
        migrations.AlterField(
            model_name='classes',
            name='level',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='classes',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
