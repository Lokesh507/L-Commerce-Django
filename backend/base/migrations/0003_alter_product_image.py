# Generated by Django 5.1.2 on 2024-11-12 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
    ]