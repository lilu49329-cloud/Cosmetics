import django.db.models.deletion
from django.db import migrations, models

import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005b_brand_data_migration'),
    ]
    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.brand', verbose_name='Thương hiệu'),
        ),
    ]