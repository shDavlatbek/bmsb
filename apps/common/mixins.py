from django.utils.text import slugify
from rest_framework import exceptions
from modeltranslation.admin import TabbedTranslationAdmin
from django.db.models import QuerySet


class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ActiveModelMixin:
    """
    A mixin to filter out inactive records automatically.
    Must be used with models that inherit from BaseModel.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(qs.model, 'is_active'):
            return qs.filter(is_active=True)
        return qs


class IsActiveFilterMixin:
    """
    A mixin for DRF views to handle is_active filtering.
    Allows clients to include inactive records if they have the right permissions.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Check if model has is_active field
        if not hasattr(qs.model, 'is_active'):
            return qs
            
        # By default, only show active records
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        
        # Only allow staff/admin to see inactive records
        if show_inactive and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_active=True)


class SlugifyMixin:
    slug_field = 'slug'
    slug_source = 'name'
    
    def save(self, *args, **kwargs):
        if not getattr(self, self.slug_field):
            source_value = getattr(self, self.slug_source)
            setattr(self, self.slug_field, slugify(source_value))
        return super().save(*args, **kwargs) 
    

class SchoolScopedMixin:
    school_field: str | None = "school"

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self.request, "school", None) and self.school_field:
            return qs.filter(**{self.school_field: self.request.school})
        return qs

    def perform_create(self, serializer):
        if getattr(self.request, "school", None) and self.school_field:
            serializer.save(**{self.school_field: self.request.school})
        else:
            serializer.save()

    def perform_update(self, serializer):
        if getattr(self.request, "school", None) and self.school_field:
            serializer.save(**{self.school_field: self.request.school})
        else:
            serializer.save()

    def get_object(self):
        obj = super().get_object()
        req_school = getattr(self.request, "school", None)

        if req_school and self.school_field:
            if getattr(obj, f"{self.school_field}_id", None) != req_school.id:
                raise exceptions.PermissionDenied("Forbidden for this tenant.")

        elif req_school is not None and self.school_field is None:
            if obj.pk != req_school.id:
                raise exceptions.PermissionDenied("Forbidden for this tenant.")

        return obj


class DescriptionMixin:
    class Media:
        js = ("js/admin_description.js",)


class SchoolAdminMixin:
    return_all: bool = False
    def _is_school_admin(self, request):
        return (
            request.user.is_authenticated
            and not request.user.is_superuser
            and request.user.school_id is not None
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_school_admin(request):
            if self.model._meta.model_name == "school":
                return qs.filter(pk=request.user.school_id)
            return qs.filter(school=request.user.school_id)
        else:
            if self.return_all:
                return qs
            else:
                if self.model._meta.model_name == "school":
                    return qs
                return qs.filter(school=None)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school" and self._is_school_admin(request):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                pk=request.user.school.pk
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if (self._is_school_admin(request) or not self.return_all) and "school" in [f.name for f in self.model._meta.fields]:
            ro.append("school")
        return ro
    
    def get_changeform_initial_data(self, request):
        if self._is_school_admin(request) and hasattr(self.model, "school"):
            return {"school": request.user.school_id}
        return super().get_changeform_initial_data(request)

    def save_model(self, request, obj, form, change):
        if (self._is_school_admin(request) or not self.return_all) and hasattr(obj, "school"):
            obj.school = request.user.school
        super().save_model(request, obj, form, change)
        
        
class AdminTranslation(TabbedTranslationAdmin):
    class Media:
        css = {
            "all": ("css/admin_translation.css",),
        }