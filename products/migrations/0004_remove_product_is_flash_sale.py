from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0003_news_image'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_flash_sale',
        ),
    ]
