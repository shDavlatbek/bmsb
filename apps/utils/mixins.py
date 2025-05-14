from django.utils.text import slugify


class SlugifyMixin:
    """
    Mixin to automatically generate a slug from another field.
    """
    
    slug_field = 'slug'  # Field to store the slug
    slug_source = 'name'  # Field to generate the slug from
    
    def save(self, *args, **kwargs):
        if not getattr(self, self.slug_field):
            source_value = getattr(self, self.slug_source)
            setattr(self, self.slug_field, slugify(source_value))
        return super().save(*args, **kwargs) 