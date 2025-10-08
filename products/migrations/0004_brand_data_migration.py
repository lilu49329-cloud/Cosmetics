from django.db import migrations, models

def migrate_brand_text_to_fk(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Brand = apps.get_model('products', 'Brand')
    db_alias = schema_editor.connection.alias
    # Lấy tất cả giá trị brand cũ (text)
    brand_names = Product.objects.using(db_alias).values_list('brand', flat=True).distinct()
    brand_map = {}
    for name in brand_names:
        if name:
            brand_obj, created = Brand.objects.using(db_alias).get_or_create(name=name)
            brand_map[name] = brand_obj.id
    # Gán lại brand cho Product
    for product in Product.objects.using(db_alias).all():
        if product.brand and product.brand in brand_map:
            product.brand_id = brand_map[product.brand]
            product.save(update_fields=['brand'])

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_create_brand_model'),
    ]
    operations = [
        migrations.RunPython(migrate_brand_text_to_fk, reverse_code=migrations.RunPython.noop),
    ]
