# Generated by Django 4.0.3 on 2022-09-29 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Local Delicacies', 'Local Delicacies'), ('Foriegn Delicacies', 'Foriegn Delicacies'), ('Medicinal Drinks', 'Medicinal Drinks'), ('Wines & Alcohol', 'Wines & Alcohol')], max_length=200)),
                ('img', models.ImageField(blank=True, upload_to='FOOD/')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=750)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dis_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('label', models.CharField(blank=True, choices=[('Local Delicacies', 'Local Delicacies'), ('Foriegn Delicacies', 'Foriegn Delicacies'), ('Medicinal Drinks', 'Medicinal Drinks'), ('Wines & Alcohol', 'Wines & Alcohol')], max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]