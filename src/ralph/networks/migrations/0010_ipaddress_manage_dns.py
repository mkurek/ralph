# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks', '0009_auto_20160823_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaddress',
            name='manage_dns',
            field=models.BooleanField(default=True, verbose_name='Manage DNS'),
        ),
    ]
