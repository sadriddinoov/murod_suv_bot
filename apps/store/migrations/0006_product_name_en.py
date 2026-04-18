from django.db import migrations, models


def copy_existing_product_name_to_english(apps, schema_editor):
    Product = apps.get_model("store", "Product")

    for product in Product.objects.filter(name_en__isnull=True):
        product.name_en = product.name
        product.save(update_fields=["name_en"])


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_alter_orderitem_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RunPython(
            copy_existing_product_name_to_english,
            migrations.RunPython.noop,
        ),
    ]
