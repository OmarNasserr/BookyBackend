# Generated by Django 4.1.4 on 2022-12-20 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("playground_app", "0007_alter_playground_created_at_and_more"),
        ("location_app", "0002_remove_cities_number_of_playgrounds"),
    ]

    operations = [
        migrations.RenameModel(old_name="Cities", new_name="City",),
    ]
