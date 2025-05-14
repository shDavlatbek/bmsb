from modeltranslation.admin import TabbedTranslationAdmin, TranslationAdmin



class AdminTranslation(TabbedTranslationAdmin):
    class Media:
        css = {
            "all": ("css/admin_translation.css",),
        }
        

class DescriptionMixin:
    class Media:
        js = ("js/admin_description.js",)





