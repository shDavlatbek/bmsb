# 🤖 AI Assistant Guide for BMSB Project

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Architecture Fundamentals](#-architecture-fundamentals) 
- [Critical Rules & Patterns](#-critical-rules--patterns)
- [Code Templates & Examples](#-code-templates--examples)
- [Common Tasks & Solutions](#-common-tasks--solutions)
- [Testing & Debugging](#-testing--debugging)
- [Troubleshooting Guide](#-troubleshooting-guide)

---

## 🎯 Project Overview

**BMSB** is a **multi-tenant school management system** where each school operates in complete isolation using subdomain-based tenancy. Built with Django + DRF + Multi-language support.

### Key Characteristics:
- **Multi-Tenant**: Each school has its own subdomain (`school1.example.com`)
- **Internationalized**: Uzbek (default), Russian, English support
- **Security-First**: Multiple layers of data isolation and permission checks
- **Mixin-Based**: Reusable security and functionality components

### Project Structure:
```
bmsb/
├── apps/
│   ├── common/          # 🔧 Base models, mixins, utilities
│   ├── main/            # 🏫 Core school functionality (School, Direction, Teacher)
│   ├── news/            # 📰 News and announcements
│   ├── media/           # 📷 Media collections, images, videos  
│   ├── user/            # 👤 User management
│   └── resource/        # 📚 Educational resources
├── config/              # ⚙️ Settings, URLs, middleware
├── assets/              # 🎨 Static files (CSS, JS, TinyMCE)
└── requirements/        # 📦 Dependencies
```

---

## 🏗️ Architecture Fundamentals

### 1. Multi-Tenant Flow
```
1. Request → SubdomainMiddleware → Extract school from subdomain
2. Middleware → Sets request.school context  
3. View → Mixins automatically filter data by school
4. Response → Only current school's data accessible
```

### 2. Data Models Hierarchy
```
School (Tenant Root)
├── News, Banners, SchoolLife  
├── DirectionSchool → Directions
├── Teachers → Directions (M2M)
├── MediaCollections → MediaImages
└── Menus (Hierarchical MPTT)
```

### 3. Security Layers
1. **Middleware**: Subdomain → School resolution
2. **Mixins**: Automatic data filtering and permission checks  
3. **Admin**: Role-based access with school scoping
4. **Database**: Unique constraints and proper foreign keys

---

## 🚨 Critical Rules & Patterns

### NEVER BREAK THESE RULES:

#### 1. **Always Use Security Mixins**
```python
# ✅ CORRECT - Public API view
class NewsListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()

# ❌ WRONG - No security mixins
class NewsListView(ListAPIView):
    queryset = News.objects.all()
```

#### 2. **Always Use SchoolAdminMixin in Admin**
```python
# ✅ CORRECT
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, AdminTranslation):
    pass

# ❌ WRONG - Cross-tenant data leakage
@admin.register(News) 
class NewsAdmin(admin.ModelAdmin):
    pass
```

#### 3. **School Field Configuration**
```python
# ✅ CORRECT - Direct school relationship
class TeacherView(SchoolScopedMixin, ListAPIView):
    school_field = "school"

# ✅ CORRECT - Nested relationship  
class MediaImageView(SchoolScopedMixin, ListAPIView):
    school_field = "collection__school"

# ✅ CORRECT - School model itself
class SchoolView(SchoolScopedMixin, RetrieveAPIView):
    school_field = None
```

#### 4. **Model Inheritance Pattern**
```python
# ✅ CORRECT - Standard model
class YourModel(SlugifyMixin, BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # ... other fields

# ✅ CORRECT - No school field (like Subject, MusicalInstrument)
class GlobalModel(SlugifyMixin, BaseModel):
    # ... fields without school FK
```

#### 5. **Admin Best Practices**
```python
# ✅ CORRECT - Simple admin without fieldsets
@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')  # No 'school' field
    list_filter = ('is_active', 'created_at')  # No 'school' filter
    search_fields = ('title', 'description')
    # No fieldsets needed - let Django handle the form

# ❌ WRONG - Including school in display/filters
@admin.register(YourModel)
class BadAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'school', 'is_active')  # Don't show school
    list_filter = ('is_active', 'school')  # Don't filter by school
    fieldsets = (...)  # Avoid fieldsets for simple models
```

### Mixin Usage Matrix:

| Scenario | IsActiveFilterMixin | SchoolScopedMixin | SchoolAdminMixin | Admin Best Practices |
|----------|:------------------:|:-----------------:|:----------------:|:-------------------:|
| Public API | ✅ Always | ✅ If school-related | N/A | N/A |
| Admin Interface | ❌ No | N/A | ✅ Always | No fieldsets, No school in list_display/filter |
| Internal API | 🔶 Optional | ✅ If school-related | N/A | N/A |
| Global Data (Subject) | ✅ Yes | ❌ No | ❌ No | N/A |

---

## 🧩 Code Templates & Examples

### Model Template
```python
from apps.common.models import BaseModel
from apps.common.mixins import SlugifyMixin
from tinymce.models import HTMLField

class YourModel(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,  # Only if optional
        verbose_name="Maktab",
        related_name="your_models"
    )
    
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    
    # SlugifyMixin configuration
    slug_field = 'slug'      # Default
    slug_source = 'name'     # Default
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Your Model "
        verbose_name_plural = "Your Models"
        # Add unique constraint for school-scoped slugs
        unique_together = [['school', 'slug']]  # If school-related
```

### View Templates
```python
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin

# Standard List View
class YourModelListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    school_field = "school"  # Adjust based on model

# Detail View with Slug
class YourModelDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelDetailSerializer
    lookup_field = 'slug'
    school_field = "school"

# Custom Queryset (like Direction)
class DirectionListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = Direction.objects.all()
    
    def get_queryset(self):
        if hasattr(self.request, 'school') and self.request.school:
            direction_school = DirectionSchool.objects.filter(
                school=self.request.school, is_active=True
            ).first()
            if direction_school:
                direction_ids = direction_school.directions.values_list('id', flat=True)
                qs = Direction.objects.filter(id__in=direction_ids)
                return self.apply_active_filter(qs)
        return Direction.objects.none()
    
    def apply_active_filter(self, qs):
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        if show_inactive and self.request.user.is_staff:
            return qs
        return qs.filter(is_active=True)
```

### Admin Templates
```python
from django.contrib import admin
from apps.common.mixins import SchoolAdminMixin, AdminTranslation, DescriptionMixin

# Standard Admin
@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

# Rich Text Admin
@admin.register(Article)
class ArticleAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

# Special Permissions Admin
@admin.register(School)
class SchoolAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('name', 'domain', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'domain')
    
    fieldsets = (
        ('Asosiy 📌', {
            'fields': ('is_active', 'domain', 'name', 'slug', 'description')
        }),
        ('Kontaktlar 📞', {
            'fields': ('email', 'phone_number', 'address')
        }),
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
```

### Serializer Templates
```python
from rest_framework import serializers

class YourModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = ['id', 'name', 'slug', 'created_at']

class YourModelDetailSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = YourModel
        fields = [
            'id', 'name', 'slug', 'description', 
            'school_name', 'created_at'
        ]

# For relationships
class RelatedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedModel
        fields = ['id', 'name', 'slug']

class YourModelWithRelationsSerializer(YourModelDetailSerializer):
    related_items = RelatedModelSerializer(many=True, read_only=True)
    
    class Meta(YourModelDetailSerializer.Meta):
        fields = YourModelDetailSerializer.Meta.fields + ['related_items']
```

---

## 📋 Common Tasks & Solutions

### 1. Creating New App with School-Scoped Model

**Step-by-step process:**
```bash
1. python manage.py startapp your_app
2. Add to INSTALLED_APPS in config/settings/base.py
3. Create models with proper mixins
4. Create admin with proper mixins  
5. Create views with proper mixins
6. Create serializers
7. Add URLs to config/urls.py
8. Create migration: python manage.py makemigrations
9. Apply migration: python manage.py migrate
10. Test with multiple schools
```

### 2. Adding Translation Support
```python
# 1. In translation.py
from modeltranslation.translator import translator, TranslationOptions

class YourModelTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(YourModel, YourModelTranslationOptions)

# 2. Add to MODELTRANSLATION_TRANSLATION_FILES in settings
MODELTRANSLATION_TRANSLATION_FILES = (
    'apps.your_app.translation',
    # ... existing files
)
```

### 3. Custom School Filtering (Complex Relationships)
```python
class ComplexView(IsActiveFilterMixin, generics.ListAPIView):
    def get_queryset(self):
        if not (hasattr(self.request, 'school') and self.request.school):
            return Model.objects.none()
        
        # Complex filtering logic
        school = self.request.school
        qs = Model.objects.filter(
            # Your complex filter logic here
            related_field__school=school
        )
        
        # Apply active filtering manually
        return self.apply_active_filter(qs)
```

### 4. Signal for Auto-Creation
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=School)
def create_school_defaults(sender, instance, created, **kwargs):
    if created:
        # Create default instances
        YourModel.objects.create(
            school=instance,
            name="Default Name"
        )
```

### 5. Unique Constraints for Multi-Tenant
```python
class YourModel(BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    slug = models.SlugField()
    
    class Meta:
        # Ensure uniqueness per school
        unique_together = [['school', 'slug']]
        # OR use constraints for more complex cases
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'], 
                name='unique_slug_per_school'
            )
        ]
```

---

## 🧪 Testing & Debugging

### Multi-Tenant Testing Pattern
```python
from django.test import TestCase, Client

class MultiTenantTestCase(TestCase):
    def setUp(self):
        self.school1 = School.objects.create(name="School 1", domain="school1")
        self.school2 = School.objects.create(name="School 2", domain="school2")
        
        self.client1 = Client(HTTP_HOST='school1.example.com')
        self.client2 = Client(HTTP_HOST='school2.example.com')
    
    def test_data_isolation(self):
        # Create data for school1
        obj1 = YourModel.objects.create(school=self.school1, name="Test 1")
        
        # School1 should see its data
        response1 = self.client1.get('/api/your-models/')
        self.assertEqual(len(response1.data), 1)
        
        # School2 should not see school1's data
        response2 = self.client2.get('/api/your-models/')
        self.assertEqual(len(response2.data), 0)
```

### Debug Checklist:
```python
# 1. Check request context
def your_view(request):
    print(f"School: {getattr(request, 'school', 'None')}")
    print(f"Subdomain: {getattr(request, 'subdomain', 'None')}")

# 2. Check queryset SQL
def get_queryset(self):
    qs = super().get_queryset()
    print(f"SQL: {qs.query}")
    return qs

# 3. Check mixin application
class YourView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    def get_queryset(self):
        print(f"MRO: {self.__class__.__mro__}")
        return super().get_queryset()
```

---

## 🔧 Troubleshooting Guide

### Common Issues & Solutions:

#### 1. "No School Context" Error
**Problem**: Views returning empty data or permission errors
```python
# ❌ Wrong - No school context
class BadView(ListAPIView):
    queryset = YourModel.objects.all()

# ✅ Solution - Add proper mixins
class GoodView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = YourModel.objects.all()
    school_field = "school"
```

#### 2. "Cross-Tenant Data Leakage"  
**Problem**: Users see data from other schools
```python
# ❌ Wrong - Manual filtering
def get_queryset(self):
    return YourModel.objects.filter(school__domain=self.request.subdomain)

# ✅ Solution - Use mixins
class SecureView(SchoolScopedMixin, ListAPIView):
    school_field = "school"  # Automatic filtering
```

#### 3. "Admin Shows All Data"
**Problem**: School admins see data from all schools
```python
# ❌ Wrong
@admin.register(YourModel)
class BadAdmin(admin.ModelAdmin):
    pass

# ✅ Solution
@admin.register(YourModel)
class GoodAdmin(SchoolAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')  # No 'school' field
    list_filter = ('is_active', 'created_at')  # No 'school' filter
    search_fields = ('title',)
    # Note: No fieldsets needed - school filtering is automatic
```

#### 4. "Admin Fieldsets Issues"
**Problem**: Using fieldsets when not needed
```python
# ❌ Wrong - Unnecessary fieldsets for simple models
@admin.register(YourModel)
class BadAdmin(SchoolAdminMixin, AdminTranslation):
    fieldsets = (
        ('Basic Info', {'fields': ('school', 'title')}),
    )

# ✅ Solution - Let Django handle the form layout
@admin.register(YourModel)
class GoodAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    # No fieldsets needed for simple models

# 📝 Note: Fieldsets are only useful for complex models with many fields
# Example: School model with contact info, social links, etc.
@admin.register(School)
class SchoolAdmin(SchoolAdminMixin, AdminTranslation):
    fieldsets = (
        ('Asosiy 📌', {'fields': ('name', 'domain', 'description')}),
        ('Kontaktlar 📞', {'fields': ('email', 'phone_number', 'address')}),
        ('Ijtimoiy tarmoqlar 🔗', {'fields': ('instagram_link', 'telegram_link')}),
    )
```

#### 5. "School Field in Admin List/Filters"
**Problem**: Including school in list_display or list_filter
```python
# ❌ Wrong - School field shown to users
@admin.register(YourModel)
class BadAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'school', 'is_active')  # Shows school
    list_filter = ('is_active', 'school')  # Allows filtering by school

# ✅ Solution - School filtering is automatic
@admin.register(YourModel)
class GoodAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')  # No school
    list_filter = ('is_active', 'created_at')  # No school filter
```

---

## 🎯 AI Assistant Decision Framework

### When implementing new features, always ask:

1. **Is this school-scoped?** → Use `SchoolScopedMixin`
2. **Is this public-facing?** → Use `IsActiveFilterMixin`  
3. **Is this an admin interface?** → Use `SchoolAdminMixin`
4. **Should this be translated?** → Add translation support
5. **Does this need a slug?** → Use `SlugifyMixin`

### Priority Order for Problem Solving:

1. **Security First**: Ensure proper tenant isolation
2. **Follow Patterns**: Use existing mixins and templates
3. **Test Multi-Tenant**: Verify isolation between schools
4. **Check Documentation**: Reference existing guides
5. **Maintain Consistency**: Follow project conventions

### Code Review Checklist:

- [ ] Proper mixin usage for security
- [ ] Correct school field configuration  
- [ ] Translation support where needed
- [ ] Admin interface properly configured (no school in list_display/filter)
- [ ] No unnecessary fieldsets in admin
- [ ] Tests include multi-tenant scenarios
- [ ] No cross-tenant data leakage
- [ ] Follows project naming conventions
- [ ] Documentation updated if needed

---

**Remember**: BMSB is security-first, multi-tenant system. Every piece of code must respect tenant boundaries and use the established patterns. When in doubt, favor more security mixins rather than fewer! 