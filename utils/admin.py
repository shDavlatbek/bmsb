from modeltranslation.admin import TabbedTranslationAdmin

class AdminTranslation(TabbedTranslationAdmin):
    class Media:
        css = {
            "all": ("css/admin_translation.css",),
        }