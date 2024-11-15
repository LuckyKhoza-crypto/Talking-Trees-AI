# Generated by Django 4.2.5 on 2024-03-15 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='trees_Database',
            fields=[
                ('id', models.CharField(max_length=5, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('altitude_ft', models.FloatField(null=True)),
                ('tree_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('zone', models.CharField(max_length=2, null=True)),
                ('group_name', models.CharField(max_length=50, null=True)),
                ('leaf_fall', models.CharField(max_length=50, null=True)),
                ('common_name', models.CharField(max_length=255, null=True)),
                ('genus', models.CharField(max_length=50, null=True)),
                ('species_name', models.CharField(max_length=255, null=True)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('cbh', models.FloatField(null=True)),
                ('dbh', models.FloatField(null=True)),
                ('tree_height_ft', models.FloatField(null=True)),
                ('canopy_radius_ft', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'whitman_trees',
            },
        ),
    ]
