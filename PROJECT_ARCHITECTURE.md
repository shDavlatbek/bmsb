# BMSB Project Architecture & Developer Guide

## 🏗️ Project Overview

BMSB is a **multi-tenant school management system** built with Django and Django REST Framework. The system uses **subdomain-based multi-tenancy** where each school gets its own subdomain (e.g., `school1.example.com`, `school2.example.com`).

## 📁 Project Structure

```
bmsb/
├── apps/                   # Django applications
│   ├── common/            # Shared utilities, mixins, base models
│   ├── main/              # Core school functionality
│   ├── news/              # News and announcements
│   ├── media/             # Media management
│   ├── user/              # User management
│   └── resource/          # Educational resources
├── config/                # Project configuration
│   ├── settings/          # Environment-specific settings
│   ├── swagger/           # API documentation
│   └── urls.py           # Main URL routing
├── assets/                # Static assets (CSS, JS, TinyMCE)
├── media/                 # User-uploaded files
└── requirements/          # Dependencies
```

## 🎯 Key Architectural Patterns

### 1. Multi-Tenant Architecture
- **Subdomain-based tenancy**: Each school gets a unique subdomain
- **Middleware-driven**: `SubdomainMiddleware` resolves school from subdomain
- **Data isolation**: School-scoped data access through mixins

### 2. Internationalization (i18n)
- **Multi-language support**: Uzbek (default), Russian, English
- **Model translation**: Using `django-modeltranslation`
- **Admin interface**: Tabbed translation interface

### 3. Content Management
- **Rich text editing**: TinyMCE integration
- **Image optimization**: Automatic image compression
- **Media management**: Organized file uploads

## 🧩 Core Mixins & Their Usage

### Model Mixins

#### `BaseModel` (Abstract Model)
```python
from apps.common.models import BaseModel

class YourModel(BaseModel):
    # Your fields here
    pass
```
**Features:**
- `created_at`, `updated_at` timestamps
- `is_active` soft deletion
- Custom `ActiveManager` and `ActiveQuerySet`

#### `SlugifyMixin`
```python
from apps.common.mixins import SlugifyMixin

class YourModel(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    slug_field = 'slug'      # Default
    slug_source = 'name'     # Default
```
**Auto-generates slugs** from specified source field.

### View Mixins

#### `IsActiveFilterMixin` 🔥 **CRITICAL**
```python
from apps.common.mixins import IsActiveFilterMixin

class YourListView(IsActiveFilterMixin, ListAPIView):
    # Only active records by default
    # Staff can see inactive with ?show_inactive=true
```
**Usage Rules:**
- ✅ **ALWAYS** use for public-facing views
- ✅ Use for admin views that need active filtering
- ❌ Don't use for internal management views

#### `SchoolScopedMixin` 🔥 **CRITICAL**
```python
from apps.common.mixins import SchoolScopedMixin

class YourView(SchoolScopedMixin, ListAPIView):
    school_field = "school"    # Default
    return_all = False         # Default
```
**Features:**
- Automatically filters by current school
- Handles CRUD operations with school assignment
- Permission checks for cross-tenant access

**Configuration Options:**
- `school_field = "school"` - Foreign key field name to school
- `school_field = None` - For School model itself
- `return_all = True` - For superuser views that need all data

### Admin Mixins

#### `SchoolAdminMixin` 🔥 **CRITICAL**
```python
from apps.common.mixins import SchoolAdminMixin

@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, admin.ModelAdmin):
    return_all = False  # Default - shows only current school's data
```
**Features:**
- Multi-tenant admin interface
- Auto-assigns school on save
- Filters querysets by user's school
- Makes school field readonly for school admins

#### `AdminTranslation`
```python
from apps.common.mixins import AdminTranslation

@admin.register(YourModel)
class YourModelAdmin(AdminTranslation):
    # Automatic tabbed translation interface
```

#### `DescriptionMixin`
```python
from apps.common.mixins import DescriptionMixin

@admin.register(YourModel)
class YourModelAdmin(DescriptionMixin, admin.ModelAdmin):
    # Enhanced description field handling in admin
```

## 📋 Developer Guidelines

### 🚨 CRITICAL Rules - NEVER BREAK

1. **Always use `SchoolScopedMixin`** for school-related data views
2. **Always use `IsActiveFilterMixin`** for public views
3. **Always use `SchoolAdminMixin`** for school-related admin classes
4. **Never expose cross-tenant data** without explicit permission
5. **Always validate school ownership** in custom logic

### 🔧 When to Use Each Mixin

#### In Views (DRF)
```python
# ✅ Standard school-scoped list view
class NewsListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = News.objects.all()

# ✅ Detail view with tenant check
class NewsDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    lookup_field = 'slug'

# ✅ Superuser view that sees all data
class AllSchoolsView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    return_all = True
    permission_classes = [IsAdminUser]

# ✅ School model view (no school_field needed)
class SchoolView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    school_field = None
```

#### In Admin
```python
# ✅ Standard school-scoped admin
@admin.register(News)
class NewsAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'school', 'is_active')

# ✅ School admin with special permissions
@admin.register(School)
class SchoolAdmin(SchoolAdminMixin, AdminTranslation):
    return_all = False  # School admins see only their school
    
    def has_add_permission(self, request):
        return request.user.is_superuser

# ✅ Rich text content admin
@admin.register(Article)
class ArticleAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    pass
```

#### In Models
```python
# ✅ Standard school-related model
class News(BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
# ✅ Model with auto-slug
class Category(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
```

### 🛡️ Security Considerations

1. **Tenant Isolation**
   - Never bypass `SchoolScopedMixin` for school data
   - Always validate school ownership in custom views
   - Use `return_all=True` only for superuser functionality

2. **Active Record Filtering**
   - Public APIs must use `IsActiveFilterMixin`
   - Admin interfaces can show inactive records
   - Use `?show_inactive=true` for staff debugging

3. **Permission Layers**
   ```python
   # Multiple security layers
   class SecureView(IsActiveFilterMixin, SchoolScopedMixin, CreateAPIView):
       permission_classes = [IsAuthenticated, IsSchoolMember]
   ```

### 📝 Common Patterns

#### Custom Filter Backends
```python
class CategorySlugFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_slug = request.query_params.get('category_slug')
        if category_slug:
            return queryset.filter(category__slug=category_slug)
        return queryset
```

#### View Count Tracking
```python
class NewsDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()  # Custom method
        return super().retrieve(request, *args, **kwargs)
```

#### Fieldset Organization (Admin)
```python
@admin.register(School)
class SchoolAdmin(SchoolAdminMixin, AdminTranslation):
    fieldsets = (
        ('Asosiy 📌', {'fields': ('is_active', 'name', 'domain')}),
        ('Raqamlar 📊', {'fields': ('student_count', 'teacher_count')}),
        ('Kontaktlar 📞', {'fields': ('email', 'phone_number')}),
    )
```

### 🚫 Anti-Patterns (DON'T DO)

```python
# ❌ Missing tenant isolation
class BadNewsView(ListAPIView):
    queryset = News.objects.all()  # Exposes all schools' data!

# ❌ Missing active filtering
class BadPublicView(SchoolScopedMixin, ListAPIView):
    # No IsActiveFilterMixin - shows inactive records!

# ❌ Bypassing mixins in admin
@admin.register(News)
class BadNewsAdmin(admin.ModelAdmin):
    # No SchoolAdminMixin - shows all schools' data!

# ❌ Manual school filtering
class BadView(APIView):
    def get(self, request):
        # Manual filtering instead of using mixins
        if request.school:
            news = News.objects.filter(school=request.school)
```

### 🔄 Migration Considerations

When adding new school-related models:

1. **Always include school foreign key**
2. **Inherit from BaseModel**
3. **Add admin with SchoolAdminMixin**
4. **Create views with proper mixins**
5. **Add to translation files if needed**

### 🧪 Testing Guidelines

```python
# Test with school context
class NewsViewTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School", domain="test")
        self.client.defaults['HTTP_HOST'] = 'test.example.com'
    
    def test_school_scoped_view(self):
        # Test that view only returns school's data
        response = self.client.get('/api/news/')
        # Assertions...
```

## 🚀 Quick Start for New Developers

1. **Study the mixins** in `apps/common/mixins.py`
2. **Follow existing patterns** in `apps/main/` and `apps/news/`
3. **Always use the security mixins** for new views and admin
4. **Test with multiple schools** to ensure proper isolation
5. **Check admin interface** works correctly for school admins

## 📚 Key Dependencies

- **Django 5.2+** - Web framework
- **Django REST Framework** - API framework
- **django-modeltranslation** - Model translation
- **django-mptt** - Tree structures (menus)
- **django-jazzmin** - Admin interface
- **django-tinymce** - Rich text editor
- **django-cors-headers** - CORS handling
- **django-filters** - API filtering

Remember: **Security through mixins, consistency through patterns!** 🔒 