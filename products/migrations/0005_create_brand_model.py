from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0004_remove_product_is_flash_sale'),
    ]
    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Tên thương hiệu')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Logo thương hiệu')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
    ]