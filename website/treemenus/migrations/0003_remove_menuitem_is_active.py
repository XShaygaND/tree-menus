# Generated by Django 5.0.2 on 2024-02-13 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treemenus', '0002_remove_menuitem_menu_menuitem_name_delete_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='is_active',
        ),
    ]