from modeltranslation.translator import register, TranslationOptions
from apps.news.models import News, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content') 