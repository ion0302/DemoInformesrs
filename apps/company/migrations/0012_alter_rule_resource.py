# Generated by Django 3.2.12 on 2022-04-19 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_alter_planlog_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='resource',
            field=models.CharField(choices=[('COMPANY.LIST', 'Company.list'), ('COMPANY.RETRIEVE', 'Company.retrieve'), ('COMPANY.PARTIAL_UPDATE', 'Company.partial_update'), ('COMPANY.UPDATE', 'Company.update'), ('COMPANY.DELETE', 'Company.delete'), ('COMPANY.TEST_ACTION', 'Company.test_action')], max_length=100),
        ),
    ]
