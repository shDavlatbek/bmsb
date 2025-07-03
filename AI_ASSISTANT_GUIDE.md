# 🤖 AI Assistant Guide for BMSB Project

## 🤖 **INSTRUCTIONS FOR AI ASSISTANTS**

**READ THIS FIRST** - These are mandatory rules for all AI assistants working on this project:

### **Core Principles:**
1. **NEVER** include `school` in `list_display` or `list_filter` in admin interfaces
2. **NEVER** use `fieldsets` in admin unless the model has 10+ fields that need grouping
3. **ALWAYS** use security mixins: `SchoolAdminMixin`, `SchoolScopedMixin`, `IsActiveFilterMixin`
4. **ALWAYS** include translation support for user-facing text fields
5. **ALWAYS** use established patterns - refer to examples in this document
6. **IMPORTANT**: School field should ONLY be in models - NEVER include `school` field in serializers (it's automatically filtered by mixins)
7. **ALWAYS** add `constraints = [models.UniqueConstraint(...)]` for school-scoped models when needed
8. **NEVER** use `unique=True` on slug fields - use constraints instead
9. **ALWAYS** check `/api/docs/` after API changes to ensure documentation is updated

### **Constraints Rule (Updated):**
- **Models with school + slug**: 
  ```python
  constraints = [
      models.UniqueConstraint(
          fields=['school', 'slug'],
          name='unique_modelname_school_slug',
      )
  ]
  ```
- **Models with school + title (no slug)**: **NO CONSTRAINTS** - Allow duplicate titles per school
- **Global models** (Subject, MusicalInstrument): 
  ```python
  constraints = [
      models.UniqueConstraint(
          fields=['slug'],
          name='unique_modelname_slug',
      )
  ]
  ```
- **Only add constraints IF NEEDED** - not all models require uniqueness constraints

### **Quick Reference Commands:**
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Check system: `python manage.py check`
- Never specify migration names unless specifically requested

### **When User Asks for New Features:**
1. Look at existing examples in this document (FAQ, Vacancy, Direction, Staff, Leader, etc.)
2. Follow the **exact same patterns**
3. Use proper Uzbek field names and verbose_name
4. Include all necessary imports
5. Create complete implementation (model + admin + serializer + view + URL)
6. **NEVER include school field in serializers** - it's handled automatically by security mixins
7. **CHECK API DOCUMENTATION** - After implementing any API endpoints, check `/api/docs/` to ensure the custom Swagger documentation is up to date

### **File Upload Handling:**
- **File conflicts**: The `generate_upload_path` function in `apps/common/utils.py` automatically handles duplicate filenames by appending an 8-character UUID suffix
- **Path format**: `<app>/<model>/<Y/m/d>/<filename>` (adds `-<8-char-uuid>` only if there's a clash)
- **Example**: `image.png` → `image-a1b2c3d4.png` if original exists

### **Middleware Updates (Header-Based School Identification):**
- **Changed**: SubdomainMiddleware now uses header-based school identification instead of URL parsing
- **Header Name**: `School` (e.g., `School: mk1`)
- **No Fallback**: If no header provided, school context remains `None` (no URL/subdomain checking)
- **Swagger Integration**: Global School header with default value `test` for easy API testing

---

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
- **Pattern-Consistent**: Established patterns MUST be followed for all new features
- **Mixin-Based**: Reusable security and functionality components

### **⚠️ CRITICAL**: Pattern Consistency
This project has **established patterns** that must be followed exactly. All new features should look and behave identically to existing ones. Refer to the **Complete Feature Implementation Example** section for the exact patterns to follow.

### Project Structure:
```
bmsb/
├── apps/
│   ├── common/          # 🔧 Base models, mixins, utilities
│   ├── main/            # 🏫 Core school functionality (School, Direction, Teacher, FAQ, Vacancy)
│   ├── news/            # 📰 News and announcements
│   ├── media/           # 📷 Media collections, images, videos  
│   ├── user/            # 👤 User management
│   └── resource/        # 📚 Educational resources (videos, files)
├── config/              # ⚙️ Settings, URLs, middleware
├── assets/              # 🎨 Static files (CSS, JS, TinyMCE)
└── requirements/        # 📦 Dependencies
```

---

## 🏗️ Architecture Fundamentals

### 1. Multi-Tenant Flow (Updated)
```
1. Request → SubdomainMiddleware → Extract school from header
2. Middleware → Sets request.school context based on 'School' header
3. View → Mixins automatically filter data by school
4. Response → Only current school's data accessible
```

#### **Header-Based School Identification**
The middleware now uses a simplified header-based approach:
- Frontend sends `School: mk1` header (where `mk1` is the school subdomain)
- No more URL/subdomain parsing - only header checking
- If no header or empty, both `request.school` and `request.subdomain` remain `None`

**Example Frontend Request:**
```javascript
fetch('https://api.example.com/api/news/', {
    headers: {
        'School': 'mk1',  // Specify the school subdomain
        'Content-Type': 'application/json'
    }
})
```

#### **Swagger UI Global Header Support**
For easy API testing, Swagger UI includes a global `School` header on all endpoints:

- **Location**: `/api/swagger/` - Available on every API endpoint
- **Description**: "Maktab subdomain (toshken1, mk1)"
- **Default Value**: `test` (for development/testing)
- **Required**: No (optional header)

**How to use in Swagger:**
1. Navigate to any API endpoint in Swagger UI
2. Find the "School" header parameter field
3. Enter the school subdomain (e.g., `mk1`, `toshken1`) or leave as `test`
4. Execute the request

This makes testing multi-tenant functionality easy without manually adding headers!

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
1. **Middleware**: Header-based school resolution (`School` header → School lookup)
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

#### 6. **SchoolAdminMixin Foreign Key Filtering**
The `SchoolAdminMixin` automatically filters **ALL foreign key fields** that have a school relationship:

```python
# ✅ AUTOMATIC FILTERING - No manual code needed
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, AdminTranslation):
    # Category dropdown will AUTOMATICALLY show only current school's categories
    # Author dropdown will AUTOMATICALLY show only current school's authors
    # Any FK with school field will be filtered automatically
    pass

# ⚠️ CRITICAL: Foreign key models MUST have school field properly populated
# Example: Categories must have school=current_school, not school=None
```

**What Gets Automatically Filtered:**
- ✅ Category field in News → Only current school's categories
- ✅ Teacher field in any model → Only current school's teachers  
- ✅ Any foreign key to a model with `school` field → Filtered by current school
- ✅ Active status → Inactive records automatically excluded
- ✅ School field itself → Limited to current user's school

#### 7. **Data Assignment Requirements** ⚠️ **CRITICAL**
**SchoolAdminMixin foreign key filtering only works when:**
- ✅ **Models have proper school assignment**: `school=actual_school` (not `None`)
- ✅ **Admin uses SchoolAdminMixin**: Automatic filtering enabled
- ✅ **Data created via admin**: `save_model` assigns school automatically

**If foreign key dropdowns show ALL records instead of school-specific ones:**
```python
# 🔍 DIAGNOSIS: Check data assignment
from apps.news.models import Category
for cat in Category.objects.all():
    print(f"{cat.name} → School: {cat.school}")
# If you see "None", that's the issue!

# 🔧 FIX: Assign proper schools to existing data
Category.objects.filter(school=None).update(school_id=1)  # Replace 1 with actual school ID
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
    slug = models.SlugField(verbose_name="Slug")
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    
    # SlugifyMixin configuration
    slug_field = 'slug'      # Default
    slug_source = 'name'     # Default
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Your Model "
        verbose_name_plural = "Your Models"
        # ALWAYS add unique constraint for school-scoped models
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_modelname_school_slug',
            )
        ]

# Alternative patterns for unique_together:

# For models with school + title (no slug):
class SimpleModel(BaseModel):
    school = models.ForeignKey('main.School', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    
    class Meta:
        verbose_name = "Simple Model"
        verbose_name_plural = "Simple Models"
        # NO CONSTRAINTS - Allow duplicate titles per school

# For hierarchical models like Menu:
class HierarchicalModel(BaseModel):
    school = models.ForeignKey('main.School', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'title', 'parent'],
                name='unique_modelname_school_title_parent',
            )
        ]

# For global models (no school field):
class GlobalModel(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(verbose_name="Slug")
    
    class Meta:
        # No unique_together needed - global data, slug is already unique
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_modelname_slug',
            )
        ]
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
8. Create and apply migrations
9. Test with multiple schools
```

### 2. Adding Translation Support
```python
# 1. In translation.py
from modeltranslation.translator import translator, TranslationOptions

class YourModelTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('uz',)

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
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'], 
                name='unique_slug_per_school'
            )
        ]
```

### 6. Complete Feature Implementation Example (Staff with Social Media)

**Model Example:**
```python
class Staff(SlugifyMixin, BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, 
                              null=True, blank=True, verbose_name="Maktab",
                              related_name="staffs")
    
    full_name = models.CharField(max_length=500, verbose_name="F.I.O")
    slug = models.SlugField(verbose_name="Slug")
    position = models.CharField(max_length=255, verbose_name="Lavozimi")
    image = models.ImageField(upload_to=generate_upload_path, 
                             verbose_name="Rasm", validators=[file_size])
    description = models.TextField(null=True, blank=True, verbose_name="Tafsilot")
    
    # Social media links
    phone_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon raqami")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    instagram_link = models.URLField(null=True, blank=True, verbose_name="Instagram havola")
    telegram_link = models.URLField(null=True, blank=True, verbose_name="Telegram havola")
    facebook_link = models.URLField(null=True, blank=True, verbose_name="Facebook havola")
    linkedin_link = models.URLField(null=True, blank=True, verbose_name="LinkedIn havola")
    
    experience_years = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tajribasi")
    
    slug_source = 'full_name'
    
    class Meta:
        verbose_name = "Xodim "
        verbose_name_plural = "Xodimlar"
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_staff_school_slug',
            )
        ]
```

**Admin Example:**
```python
@admin.register(Staff)
class StaffAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('full_name', 'position', 'experience_years', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'position', 'description')
    prepopulated_fields = {'slug': ('full_name',)}
    # No school in list_display or list_filter - automatic filtering
    # No fieldsets - simple model with reasonable field count
```

**Serializer Example (IMPORTANT - No School Field):**
```python
class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 
            'instagram_link', 'telegram_link', 'facebook_link', 'linkedin_link',
            'experience_years', 'created_at'
        ]
        # NOTE: NO 'school' field - it's automatically filtered by mixins
        # NOTE: Staff only has list view, no detail view (single page removed)

class LeaderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 
            'working_days', 'created_at'
        ]

class LeaderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 'description',
            'phone_number', 'email', 'instagram_link', 'telegram_link',
            'facebook_link', 'linkedin_link', 'working_days', 'created_at'
        ]
        # NOTE: NO 'school' field - security mixins handle school filtering
```

**View Example:**
```python
class StaffListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
    school_field = "school"  # This tells the mixin how to filter by school
    # NOTE: No detail view for Staff - only list view

class LeaderListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderListSerializer
    school_field = "school"

class LeaderDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderDetailSerializer
    lookup_field = 'slug'
    school_field = "school"
```

### 7. Honors Implementation Example (Honors & HonorAchievements)

**Model Example:**
```python
HONOR_TYPES = [
    ('student', 'Talaba'),
    ('teacher', 'O\'qituvchi'),
    ('staff', 'Xodim'),
    ('leader', 'Rahbar'),
]

class Honors(SlugifyMixin, BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE,
                              null=True, blank=True, verbose_name="Maktab",
                              related_name="honors")
    
    full_name = models.CharField(max_length=255, verbose_name="F.I.O")
    slug = models.SlugField(verbose_name="Slug")
    slug_source = "full_name"
    
    type = models.CharField(max_length=50, choices=HONOR_TYPES, 
                           default='student', verbose_name="Kim?")
    description = HTMLField(verbose_name="Tafsilot")
    image = models.ImageField(upload_to=generate_upload_path, verbose_name="Rasm",
                             validators=[file_size])
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    phone_number = models.CharField(max_length=255, null=True, blank=True, 
                                   verbose_name="Telefon raqami")
    
    class Meta:
        verbose_name = "Faxrimiz"
        verbose_name_plural = "Faxrlarimiz"
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_honors_school_slug',
            )
        ]

class HonorAchievements(BaseModel):
    honor = models.ForeignKey(Honors, on_delete=models.CASCADE,
                             verbose_name="Hojat", related_name="achievements")
    year = models.PositiveIntegerField(verbose_name="Yil")
    description = models.TextField(verbose_name="Tafsilot")
    address = models.CharField(max_length=255, verbose_name="Manzil")
```

**Serializer Example:**
```python
class HonorAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonorAchievements
        fields = ['id', 'year', 'description', 'address', 'created_at']

class HonorsListSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    type_text = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Honors
        fields = ['id', 'full_name', 'slug', 'type', 'type_text', 
                 'image', 'description', 'created_at']
    
    def get_description(self, obj):
        """Strip HTML tags and truncate to 100 characters"""
        if obj.description:
            plain_text = strip_tags(obj.description)
            return plain_text[:100] + '...' if len(plain_text) > 100 else plain_text
        return ''

class HonorsDetailSerializer(serializers.ModelSerializer):
    achievements = HonorAchievementsSerializer(many=True, read_only=True)
    type_text = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Honors
        fields = ['id', 'full_name', 'slug', 'type', 'type_text', 'description',
                 'image', 'email', 'phone_number', 'achievements', 'created_at']
```

**Admin Example:**
```python
class HonorAchievementsInline(TranslationTabularInline):
    model = HonorAchievements
    extra = 1
    fields = ('year', 'description', 'address', 'is_active')
    
    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }

@admin.register(Honors)
class HonorsAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('full_name', 'type', 'image_preview', 'is_active', 'created_at')
    list_filter = ('is_active', 'type', 'created_at')
    search_fields = ('full_name', 'description')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [HonorAchievementsInline]
    
    def image_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Rasm"
```

**Translation Configuration:**
```python
class HonorsTranslationOptions(TranslationOptions):
    fields = ('full_name', 'description')
    required_languages = ('uz',)

class HonorAchievementsTranslationOptions(TranslationOptions):
    fields = ('description', 'address')
    required_languages = ('uz',)

translator.register(Honors, HonorsTranslationOptions)
translator.register(HonorAchievements, HonorAchievementsTranslationOptions)
```

**View Example:**
```python
class HonorsListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsListSerializer
    school_field = "school"

class HonorsDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsDetailSerializer
    lookup_field = 'slug'
    school_field = "school"
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

### When implementing new features, ALWAYS follow this checklist:

1. **Is this school-scoped?** → Use `SchoolScopedMixin` with proper `school_field`
2. **Is this public-facing?** → Use `IsActiveFilterMixin`  
3. **Is this an admin interface?** → Use `SchoolAdminMixin` + `AdminTranslation`
4. **Should this be translated?** → Add translation support with required Uzbek
5. **Does this need a slug?** → Use `SlugifyMixin` with `slug_source`

### Mandatory Patterns to Follow:

#### **Model Pattern:**
```python
class YourModel(SlugifyMixin, BaseModel):  # or just BaseModel if no slug needed
    school = models.ForeignKey(School, on_delete=models.CASCADE, 
                              null=True, blank=True, verbose_name="Maktab",
                              related_name="your_models")
    title = models.CharField(max_length=255, verbose_name="Uzbek Title")
    slug = models.SlugField(verbose_name="Slug")  # if using SlugifyMixin
    
    slug_source = 'title'  # if using SlugifyMixin
    
    class Meta:
        verbose_name = "Uzbek Singular"
        verbose_name_plural = "Uzbek Plural"
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_modelname_school_slug',
            )
        ]
```

#### **Admin Pattern:**
```python
@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')  # NO school field
    list_filter = ('is_active', 'created_at')  # NO school filter
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}  # if has slug
    # NO fieldsets for simple models
```

#### **Serializer Pattern:**
```python
class YourModelSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = YourModel
        fields = ['id', 'title', 'slug', 'description', 'school_name', 'created_at']
```

#### **View Pattern:**
```python
class YourModelListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    school_field = "school"  # or "related_field__school" for nested
```

### Priority Order for Problem Solving:

1. **Security First**: Ensure proper tenant isolation
2. **Follow Established Patterns**: Use examples from this guide
3. **No Custom Logic**: Avoid custom filtering, use mixins
4. **Keep It Simple**: No fieldsets unless absolutely necessary
5. **Test Multi-Tenant**: Always verify isolation between schools

### Code Review Checklist:

- [ ] Proper mixin usage for security
- [ ] Correct school field configuration  
- [ ] Translation support where needed
- [ ] Admin interface follows patterns (no school in list_display/filter)
- [ ] No unnecessary fieldsets in admin
- [ ] No cross-tenant data leakage
- [ ] Follows project naming conventions
- [ ] Uses established URL patterns

---

**Remember**: BMSB is security-first, multi-tenant system. Every piece of code must respect tenant boundaries and use the established patterns. When in doubt, favor more security mixins rather than fewer! 

### **Complete List of Model Constraints (Updated):**

#### **Main App (`apps/main/models.py`):**
- `School`: `unique_school_domain`, `unique_school_slug` - Global school uniqueness
- `SchoolLife`: **NO CONSTRAINTS** - Allow duplicate titles per school
- `Menu`: **NO CONSTRAINTS** - Menu items can have duplicate titles
- `Banner`: **NO CONSTRAINTS** - Allow duplicate banner titles per school
- `Teacher`: `unique_teacher_school_slug` - Unique teacher slugs per school
- `FAQ`: **NO CONSTRAINTS** - Allow duplicate FAQ questions per school  
- `Document`: **NO CONSTRAINTS** - Allow duplicate document titles per school
- `Vacancy`: `unique_vacancy_school_slug` - Unique vacancy slugs per school
- `Staff`: `unique_staff_school_slug` - Unique staff slugs per school
- `Leader`: `unique_leader_school_slug` - Unique leader slugs per school
- `Honors`: `unique_honors_school_slug` - Unique honors slugs per school
- `Subject`: `unique_subject_slug` - Global subject slug uniqueness
- `MusicalInstrument`: `unique_musicalinstrument_slug` - Global instrument slug uniqueness
- `Direction`: `unique_direction_slug` - Global direction slug uniqueness

#### **News App (`apps/news/models.py`):**
- `Category`: `unique_newscategory_school_slug` - Unique category slugs per school
- `News`: `unique_news_school_slug` - Unique news slugs per school

#### **Media App (`apps/media/models.py`):**
- `MediaCollection`: `unique_mediacollection_school_slug` - Unique collection slugs per school

#### **Resource App (`apps/resource/models.py`):**
- `ResourceVideo`: **NO CONSTRAINTS** - Allow duplicate video titles per school
- `ResourceFile`: **NO CONSTRAINTS** - Allow duplicate file titles per school

#### **Models WITHOUT Constraints (No Uniqueness Needed):**
- `DocumentCategory` - Global categories, basic model
- `MediaImage`, `MediaVideo` - Child models, uniqueness handled at parent level
- `TeacherExperience` - Child model of Teacher
- `HonorAchievements` - Child model of Honors
- `User` - User model, no uniqueness constraints needed
- `DirectionSchool` - Relationship model
- `Menu` - Removed constraints as requested (titles can be duplicate)

#### **Key Changes Made:**
- ✅ **Removed** `unique=True` from ALL slug fields
- ✅ **Replaced** `unique_together` with modern `constraints` syntax
- ✅ **Removed** Menu constraints (title + parent) as requested
- ✅ **Added** constraints only where actually needed
- ✅ **Used** descriptive constraint names: `unique_modelname_field1_field2`

---

**Remember**: BMSB is security-first, multi-tenant system. Every piece of code must respect tenant boundaries and use the established patterns. When in doubt, favor more security mixins rather than fewer!

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

### When implementing new features, ALWAYS follow this checklist:

1. **Is this school-scoped?** → Use `SchoolScopedMixin` with proper `school_field`
2. **Is this public-facing?** → Use `IsActiveFilterMixin`  
3. **Is this an admin interface?** → Use `SchoolAdminMixin` + `AdminTranslation`
4. **Should this be translated?** → Add translation support with required Uzbek
5. **Does this need a slug?** → Use `SlugifyMixin` with `slug_source`

### Mandatory Patterns to Follow:

#### **Model Pattern:**
```python
class YourModel(SlugifyMixin, BaseModel):  # or just BaseModel if no slug needed
    school = models.ForeignKey(School, on_delete=models.CASCADE, 
                              null=True, blank=True, verbose_name="Maktab",
                              related_name="your_models")
    title = models.CharField(max_length=255, verbose_name="Uzbek Title")
    slug = models.SlugField(verbose_name="Slug")  # if using SlugifyMixin
    
    slug_source = 'title'  # if using SlugifyMixin
    
    class Meta:
        verbose_name = "Uzbek Singular"
        verbose_name_plural = "Uzbek Plural"
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_modelname_school_slug',
            )
        ]
```

#### **Admin Pattern:**
```python
@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active', 'created_at')  # NO school field
    list_filter = ('is_active', 'created_at')  # NO school filter
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}  # if has slug
    # NO fieldsets for simple models
```

#### **Serializer Pattern:**
```python
class YourModelSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = YourModel
        fields = ['id', 'title', 'slug', 'description', 'school_name', 'created_at']
```

#### **View Pattern:**
```python
class YourModelListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    school_field = "school"  # or "related_field__school" for nested
```

### Priority Order for Problem Solving:

1. **Security First**: Ensure proper tenant isolation
2. **Follow Established Patterns**: Use examples from this guide
3. **No Custom Logic**: Avoid custom filtering, use mixins
4. **Keep It Simple**: No fieldsets unless absolutely necessary
5. **Test Multi-Tenant**: Always verify isolation between schools

### Code Review Checklist:

- [ ] Proper mixin usage for security
- [ ] Correct school field configuration  
- [ ] Translation support where needed
- [ ] Admin interface follows patterns (no school in list_display/filter)
- [ ] No unnecessary fieldsets in admin
- [ ] No cross-tenant data leakage
- [ ] Follows project naming conventions
- [ ] Uses established URL patterns

---

**Remember**: BMSB is security-first, multi-tenant system. Every piece of code must respect tenant boundaries and use the established patterns. When in doubt, favor more security mixins rather than fewer! 

---

## 🚀 API Endpoints

### **Current API Endpoints (Complete List):**

#### **Main App (`/api/main/`):**
- **POST** `/api/main/contact-forms/` - Aloqa so'rovlarini yaratish (Create contact requests)
- **GET** `/api/main/comments/` - Maktab izohlarini ko'rish (List school comments)  
- **GET** `/api/main/comments/<id>/` - Izoh detallari (Get comment details)
- **GET** `/api/main/directions/` - Maktab yo'nalishlarini ko'rish (List school directions)
- **GET** `/api/main/directions/<slug>/` - Yo'nalish detallari (Get direction details)
- **GET** `/api/main/teachers/` - Maktab o'qituvchilarini ko'rish (List school teachers)
- **GET** `/api/main/teachers/<slug>/` - O'qituvchi detallari (Get teacher details)
- **GET** `/api/main/staffs/` - Maktab xodimlarini ko'rish (List school staff)
- **GET** `/api/main/staffs/<slug>/` - Xodim detallari (Get staff details)
- **GET** `/api/main/leaders/` - Maktab rahbarlarini ko'rish (List school leaders)
- **GET** `/api/main/leaders/<slug>/` - Rahbar detallari (Get leader details)
- **GET** `/api/main/honors/` - Maktab faxrlarini ko'rish (List school honors)
- **GET** `/api/main/honors/<slug>/` - Faxr detallari (Get honor details)
- **GET** `/api/main/faqs/` - Tez-tez so'raladigan savollar (List school FAQs)
- **GET** `/api/main/vacancies/` - Bo'sh ish o'rinlari (List school vacancies)
- **GET** `/api/main/vacancies/<slug>/` - Vakansiya detallari (Get vacancy details)
- **GET** `/api/main/documents/` - Maktab hujjatlari (List school documents)
- **GET** `/api/main/timetables/` - Dars jadvallari (List school timetables)
- **GET** `/api/main/banners/` - Maktab bannerlari (List school banners)
- **GET** `/api/main/school-lifes/` - Maktab hayoti rasmlari (List school life images)
- **GET** `/api/main/school/` - Maktab ma'lumotlari (Get school details)
- **GET** `/api/main/menus/` - Maktab menyu tuzilmasi (Get school menu structure)

#### **News App (`/api/news/`):**
- **GET** `/api/news/categories/` - Yangilik kategoriyalari (List news categories)
- **GET** `/api/news/` - Maktab yangiliklari (List school news)
- **GET** `/api/news/<slug>/` - Yangilik detallari (Get news details)

#### **Media App (`/api/media/`):**
- **GET** `/api/media/collections/` - Media kolleksiyalari (List media collections)
- **GET** `/api/media/collections/<slug>/` - Kolleksiya detallari (Get collection details)

#### **Resource App (`/api/resource/`):**
- **GET** `/api/resource/videos/` - Ta'lim videolari (List resource videos)
- **GET** `/api/resource/files/` - Ta'lim fayllari (List resource files)

#### **Authentication & Users:**
- Standard Django auth endpoints
- Custom user management through admin interface

---

## 📁 Project Files Structure

### **Core Configuration Files:**
```
config/
├── settings/
│   ├── base.py              # Asosiy sozlamalar
│   ├── development.py       # Ishlab chiqish muhiti
│   ├── production.py        # Ishlab chiqarish muhiti
│   └── testing.py          # Test muhiti
├── urls.py                  # Asosiy URL konfiguratsiyasi
├── wsgi.py                  # WSGI konfiguratsiyasi
└── asgi.py                  # ASGI konfiguratsiyasi
```

### **Main Application Files:**
```
apps/main/
├── models.py                # Barcha main model sinflari
├── admin.py                 # Admin interfeys konfiguratsiyasi
├── serializers/
│   ├── contact_form.py     # ContactForm serializer
│   ├── comments.py         # Comments serializer
│   ├── direction.py        # Direction serializer
│   ├── school.py          # School serializer
│   ├── teacher.py         # Teacher serializer
│   ├── staff.py           # Staff serializer
│   ├── leader.py          # Leader serializer
│   ├── honors.py          # Honors serializer
│   ├── faq.py             # FAQ serializer
│   ├── vacancy.py         # Vacancy serializer
│   └── ...                # Boshqa serializer fayllar
├── views/
│   ├── contact_form.py    # ContactForm ko'rinishlar
│   ├── comments.py        # Comments ko'rinishlar
│   ├── direction.py       # Direction ko'rinishlar
│   ├── school.py          # School ko'rinishlar
│   ├── teacher.py         # Teacher ko'rinishlar
│   └── ...                # Boshqa view fayllar
├── translation.py         # Tarjima konfiguratsiyasi
├── urls.py               # URL yo'nalishlar
└── migrations/           # Ma'lumotlar bazasi o'zgarishlari
```

### **Common Utilities:**
```
apps/common/
├── models.py             # BaseModel, SlugifyMixin
├── mixins.py            # SchoolScopedMixin, IsActiveFilterMixin, SchoolAdminMixin
├── utils.py             # Fayl yuklash, yordamchi funksiyalar
├── views.py             # APIDocumentationView
├── templates/
│   └── api_documentation.html  # API hujjatlash sahifasi
└── middleware.py        # Maktab konteksti middleware
```

### **News App Files:**
```
apps/news/
├── models.py            # Category, News modellari
├── admin.py             # News admin konfiguratsiyasi
├── serializers.py       # News serializer sinflari
├── views.py            # News API ko'rinishlar
├── urls.py             # News URL yo'nalishlar
├── translation.py      # News tarjima konfiguratsiyasi
└── migrations/         # News ma'lumotlar bazasi o'zgarishlari
```

### **Media App Files:**
```
apps/media/
├── models.py           # MediaCollection, MediaImage modellari
├── admin.py            # Media admin konfiguratsiyasi
├── serializers.py      # Media serializer sinflari
├── views.py           # Media API ko'rinishlar
├── urls.py            # Media URL yo'nalishlar
├── translation.py     # Media tarjima konfiguratsiyasi
└── migrations/        # Media ma'lumotlar bazasi o'zgarishlari
```

### **Resource App Files:**
```
apps/resource/
├── models.py          # ResourceVideo, ResourceFile modellari
├── admin.py           # Resource admin konfiguratsiyasi
├── serializers.py     # Resource serializer sinflari
├── views.py          # Resource API ko'rinishlar
├── urls.py           # Resource URL yo'nalishlar
├── translation.py    # Resource tarjima konfiguratsiyasi
└── migrations/       # Resource ma'lumotlar bazasi o'zgarishlari
```

### **User Management:**
```
apps/user/
├── models.py         # Foydalanuvchi modeli
├── admin.py          # User admin konfiguratsiyasi
├── views.py         # User API ko'rinishlar
├── serializers.py   # User serializer sinflari
├── urls.py          # User URL yo'nalishlar
└── migrations/      # User ma'lumotlar bazasi o'zgarishlari
```

### **Requirements Files:**
```
requirements/
├── base.txt         # Asosiy bog'liqliklar
├── development.txt  # Ishlab chiqish bog'liqliklari
└── production.txt   # Ishlab chiqarish bog'liqliklari
```

### **Static Files:**
```
assets/
├── css/            # CSS fayllar
├── js/             # JavaScript fayllar
├── images/         # Statik rasmlar
└── tinymce/        # TinyMCE redaktor fayllari
```

### **Database Migrations Status:**
- ✅ All apps have up-to-date migrations
- ✅ ContactForm and Comments models migrated successfully
- ✅ DirectionSchool translation configuration applied
- ✅ All foreign key filtering enhancements applied

### **Key Architecture Files:**
- `apps/main/middleware.py` - School context va 401 auth responses
- `apps/common/mixins.py` - Security va foreign key filtering mixins
- `config/settings/base.py` - Asosiy Django sozlamalari
- `config/urls.py` - API endpoints va admin URLs

### **Custom API Documentation (IMPORTANT):**
- **Location**: `/api/docs/` 
- **Purpose**: Beautiful, interactive API documentation in Uzbek
- **Update Required**: After adding/modifying any API endpoints, check if the documentation needs updates
- **File**: `apps/common/views.py` - `APIDocumentationView` class contains endpoint definitions
- **Template**: `apps/common/templates/api_documentation.html`
- **Features**: Live testing, Uzbek interface, organized by sections