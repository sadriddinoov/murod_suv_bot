from modeltranslation.translator import TranslationOptions, translator

from apps.store.models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Product, ProductTranslationOptions)
