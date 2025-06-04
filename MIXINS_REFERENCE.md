# BMSB Mixins Reference Guide

## 🎯 Overview

This reference provides detailed technical documentation for all mixins in the BMSB project. Each mixin serves a specific purpose in maintaining security, consistency, and functionality across the multi-tenant school management system.

## 📋 Table of Contents

- [Model Mixins](#model-mixins)
- [View Mixins](#view-mixins)
- [Admin Mixins](#admin-mixins)
- [QuerySet & Manager Mixins](#queryset--manager-mixins)
- [Implementation Examples](#implementation-examples)
- [Troubleshooting](#troubleshooting)

---

## Model Mixins

### `SlugifyMixin`
**Location**: `apps/common/mixins.py`

Automatically generates URL-friendly slugs from specified source fields.

```python
class SlugifyMixin:
    slug_field = 'slug'      # Target field name
    slug_source = 'name'     # Source field name
    
    def save(self, *args, **kwargs):
        if not getattr(self, self.slug_field):
            source_value = getattr(self, self.slug_source)
            setattr(self, self.slug_field, slugify(source_value))
        return super().save(*args, **kwargs)
```

**Usage:**
```python
class Category(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    # Custom configuration
    slug_field = 'custom_slug'  # Optional
    slug_source = 'title'       # Optional
```

**Key Features:**
- Only generates slug if field is empty
- Uses Django's `slugify()` function
- Configurable source and target fields
- Works with any CharField/SlugField

---

## View Mixins

### `IsActiveFilterMixin` 🔥
**Location**: `apps/common/mixins.py`

Filters out inactive records for public APIs while allowing staff to view them.

```python
class IsActiveFilterMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        
        if not hasattr(qs.model, 'is_active'):
            return qs
            
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        
        if show_inactive and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_active=True)
```

**Usage:**
```python
# ✅ Standard usage
class NewsListView(IsActiveFilterMixin, ListAPIView):
    queryset = News.objects.all()

# ✅ Combined with other mixins
class SchoolNewsView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
```

**Query Parameters:**
- `?show_inactive=true` - Shows inactive records (staff only)
- `?show_inactive=false` - Shows only active records (default)

**Security Notes:**
- Non-staff users always see only active records
- Staff users can choose to see inactive records
- Automatically checks for `is_active` field existence

### `SchoolScopedMixin` 🔥
**Location**: `apps/common/mixins.py`

Provides multi-tenant data isolation by automatically filtering and assigning school context.

```python
class SchoolScopedMixin:
    school_field: str | None = "school"    # FK field name
    return_all: bool = False               # Superuser override
    
    def get_queryset(self):
        # Filters by request.school
        
    def perform_create(self, serializer):
        # Auto-assigns school on creation
        
    def perform_update(self, serializer):
        # Ensures school assignment on updates
        
    def get_object(self):
        # Validates object belongs to current school
```

**Configuration Options:**
```python
class YourView(SchoolScopedMixin, ListAPIView):
    school_field = "school"           # Default - FK to School
    school_field = "department__school"  # Nested relationship
    school_field = None               # For School model itself
    return_all = True                 # Superuser sees all data
```

**Usage Examples:**
```python
# Standard school-scoped model
class NewsView(SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
    school_field = "school"  # Default

# Nested relationship
class TeacherView(SchoolScopedMixin, ListAPIView):
    queryset = Teacher.objects.all()
    school_field = "department__school"

# School model itself
class SchoolDetailView(SchoolScopedMixin, RetrieveAPIView):
    queryset = School.objects.all()
    school_field = None

# Superuser view
class AllSchoolsView(SchoolScopedMixin, ListAPIView):
    return_all = True
    permission_classes = [IsAdminUser]
```

**Security Features:**
- Automatic queryset filtering by school
- Permission checks on object access
- Auto-assignment of school on create/update
- Raises `PermissionDenied` for cross-tenant access

---

## Admin Mixins

### `SchoolAdminMixin` 🔥
**Location**: `apps/common/mixins.py`

Provides multi-tenant admin interface with school-based data isolation.

```python
class SchoolAdminMixin:
    return_all: bool = False
    
    def get_queryset(self, request):
        # Filters by user's school for school admins
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Restricts FK choices to user's school
        
    def get_readonly_fields(self, request, obj=None):
        # Makes school field readonly for school admins
        
    def save_model(self, request, obj, form, change):
        # Auto-assigns school on save
```

**Usage:**
```python
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'school', 'is_active')
    return_all = False  # School admins see only their data

@admin.register(School)
class SchoolAdmin(SchoolAdminMixin, admin.ModelAdmin):
    return_all = False  # Even for School model
    
    def has_add_permission(self, request):
        return request.user.is_superuser
```

**User Type Behavior:**
- **Superuser**: Sees all data across all schools
- **School Admin**: Sees only their school's data
- **Return All**: When `return_all=True`, shows all data for superusers

### `AdminTranslation`
**Location**: `apps/common/mixins.py`

Provides tabbed translation interface using django-modeltranslation.

```python
class AdminTranslation(TabbedTranslationAdmin):
    class Media:
        css = {
            "all": ("css/admin_translation.css",),
        }
```

**Usage:**
```python
@admin.register(News)
class NewsAdmin(AdminTranslation):
    # Automatic tabbed interface for Uzbek/Russian/English
    pass

# Combined with other mixins
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, AdminTranslation):
    pass
```

**Features:**
- Tabbed interface for each language
- Custom CSS styling
- Works with all translatable fields

### `DescriptionMixin`
**Location**: `apps/common/mixins.py`

Enhances description field handling in admin interface.

```python
class DescriptionMixin:
    class Media:
        js = ("js/admin_description.js",)
```

**Usage:**
```python
@admin.register(School)
class SchoolAdmin(DescriptionMixin, SchoolAdminMixin):
    # Enhanced description field handling
    pass
```

---

## QuerySet & Manager Mixins

### `ActiveQuerySet`
**Location**: `apps/common/models.py`

Provides filtering methods for active/inactive records.

```python
class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)
        
    def inactive(self):
        return self.filter(is_active=False)
```

### `ActiveManager`
**Location**: `apps/common/models.py`

Manager that uses ActiveQuerySet and provides default active filtering.

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)
        
    def active(self):
        return self.get_queryset().active()
        
    def inactive(self):
        return self.get_queryset().inactive()
```

**Usage:**
```python
class News(BaseModel):
    title = models.CharField(max_length=255)
    # BaseModel includes: objects = ActiveManager()

# Query examples
News.objects.all()        # All records (active by default with BaseModel)
News.objects.active()     # Only active records
News.objects.inactive()   # Only inactive records
```

### `ActiveModelMixin`
**Location**: `apps/common/mixins.py`

View mixin that automatically filters to active records only.

```python
class ActiveModelMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(qs.model, 'is_active'):
            return qs.filter(is_active=True)
        return qs
```

---

## Implementation Examples

### Complete Model Implementation
```python
# models.py
from apps.common.models import BaseModel
from apps.common.mixins import SlugifyMixin

class Category(SlugifyMixin, BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ['school', 'slug']
```

### Complete View Implementation
```python
# views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin

class CategoryListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    """
    List categories for current school.
    Supports:
    - ?show_inactive=true (staff only)
    - Automatic school filtering
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    school_field = "school"

class CategoryDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    """
    Category detail with slug lookup.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'
    school_field = "school"
```

### Complete Admin Implementation
```python
# admin.py
from django.contrib import admin
from apps.common.mixins import SchoolAdminMixin, AdminTranslation

@admin.register(Category)
class CategoryAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('name', 'school', 'slug', 'is_active')
    list_filter = ('is_active', 'school')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('school', 'name', 'slug', 'is_active')
        }),
        ('Content', {
            'fields': ('description',)
        }),
    )
```

---

## Troubleshooting

### Common Issues

#### 1. Missing School Context
**Problem**: Views return empty results or permission errors.
```python
# ❌ Wrong
class NewsView(ListAPIView):
    queryset = News.objects.all()
```

**Solution**: Add proper mixins and ensure middleware is working.
```python
# ✅ Correct
class NewsView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
```

#### 2. Cross-Tenant Data Leakage
**Problem**: Users see data from other schools.
```python
# ❌ Wrong - bypasses tenant isolation
class BadNewsView(APIView):
    def get(self, request):
        return Response(News.objects.all().values())
```

**Solution**: Always use SchoolScopedMixin.
```python
# ✅ Correct
class NewsView(SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
```

#### 3. Admin Shows Wrong Data
**Problem**: School admins see all schools' data.
```python
# ❌ Wrong
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass
```

**Solution**: Use SchoolAdminMixin.
```python
# ✅ Correct
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, admin.ModelAdmin):
    pass
```

#### 4. Inactive Records Visible
**Problem**: Public APIs show inactive records.
```python
# ❌ Wrong
class PublicNewsView(SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
```

**Solution**: Add IsActiveFilterMixin.
```python
# ✅ Correct
class PublicNewsView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()
```

### Debugging Tips

1. **Check Request Context**:
   ```python
   def get(self, request):
       print(f"School: {request.school}")
       print(f"Subdomain: {request.subdomain}")
       print(f"User: {request.user}")
   ```

2. **Verify Queryset Filtering**:
   ```python
   def get_queryset(self):
       qs = super().get_queryset()
       print(f"Queryset SQL: {qs.query}")
       return qs
   ```

3. **Test with Multiple Schools**:
   ```python
   # Create test data for different schools
   school1 = School.objects.create(name="School 1", domain="school1")
   school2 = School.objects.create(name="School 2", domain="school2")
   
   # Test isolation
   self.client.defaults['HTTP_HOST'] = 'school1.example.com'
   response = self.client.get('/api/news/')
   # Should only return school1's news
   ```

### Performance Considerations

1. **Database Queries**: SchoolScopedMixin adds WHERE clauses - ensure proper indexes.
2. **Nested Relationships**: Use `select_related()` for foreign key traversals.
3. **Translation Queries**: AdminTranslation can increase query count.

### Migration Checklist

When adding new school-related models:

- [ ] Inherit from `BaseModel`
- [ ] Add `school` foreign key
- [ ] Use `SlugifyMixin` if needed
- [ ] Create admin with `SchoolAdminMixin`
- [ ] Create views with proper mixins
- [ ] Add translation configuration
- [ ] Test multi-tenant isolation
- [ ] Verify admin permissions

Remember: **Every mixin serves a security or functionality purpose - don't skip them!** 🔒 