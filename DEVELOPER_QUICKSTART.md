# BMSB Developer Quick Start Guide

## 🚀 Welcome to BMSB!

This guide helps new developers quickly understand and contribute to the BMSB multi-tenant school management system.

## 🎯 5-Minute Overview

**What is BMSB?**
- Multi-tenant school management system
- Each school gets its own subdomain (e.g., `school1.example.com`)
- Built with Django + DRF + Multi-language support

**Key Concepts:**
- **Multi-tenancy**: Data isolation per school
- **Mixins**: Reusable security and functionality components
- **Active filtering**: Soft deletion with `is_active` field
- **Internationalization**: Uzbek/Russian/English support

## 📋 Quick Setup Checklist

### Initial Setup
- [ ] Clone repository
- [ ] Install dependencies: `pip install -r requirements/base.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Run server: `python manage.py runserver`

### Development Workflow
- [ ] Create feature branch from `main`
- [ ] Follow mixin patterns for new code
- [ ] Test with multiple schools
- [ ] Verify admin interface works
- [ ] Check translation support
- [ ] Run tests before committing

## 🧩 Code Templates

### Model Template
```python
# apps/your_app/models.py
from apps.common.models import BaseModel
from apps.common.mixins import SlugifyMixin
from django.db import models

class YourModel(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        'main.School', 
        on_delete=models.CASCADE,
        verbose_name="Maktab",
        related_name="your_models"
    )
    
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tafsilot")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Your Model"
        verbose_name_plural = "Your Models"
        unique_together = ['school', 'slug']  # Ensure slug uniqueness per school
```

### Views Template
```python
# apps/your_app/views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    """
    List view for YourModel with:
    - Active filtering
    - School scoping
    - Pagination
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = []  # Adjust as needed
    school_field = "school"

class YourModelDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    """
    Detail view with slug lookup
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    lookup_field = 'slug'

class YourModelCreateView(SchoolScopedMixin, CreateAPIView):
    """
    Create view with automatic school assignment
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = [IsAuthenticated]  # Adjust as needed
```

### Admin Template
```python
# apps/your_app/admin.py
from django.contrib import admin
from apps.common.mixins import SchoolAdminMixin, AdminTranslation
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('name', 'school', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'school', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Info 📌', {
            'fields': ('school', 'name', 'slug', 'is_active')
        }),
        ('Content 📝', {
            'fields': ('description',)
        }),
    )
    
    # Optional: Custom permissions
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete
        return request.user.is_superuser
```

### Serializer Template
```python
# apps/your_app/serializers.py
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

class YourModelDetailSerializer(YourModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta(YourModelSerializer.Meta):
        fields = YourModelSerializer.Meta.fields + ['school_name']
```

### URLs Template
```python
# apps/your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('your-models/', views.YourModelListView.as_view(), name='yourmodel-list'),
    path('your-models/<str:slug>/', views.YourModelDetailView.as_view(), name='yourmodel-detail'),
    path('your-models/create/', views.YourModelCreateView.as_view(), name='yourmodel-create'),
]
```

### Translation Template
```python
# apps/your_app/translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import YourModel

class YourModelTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # Fields to translate

translator.register(YourModel, YourModelTranslationOptions)
```

## 🔧 Common Scenarios

### Scenario 1: School-scoped Model with Categories
```python
class Category(SlugifyMixin, BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

class Article(BaseModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

# View for nested filtering
class ArticleListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Article.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs
```

### Scenario 2: Public API without Authentication
```python
class PublicNewsView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    """
    Public API - no authentication required
    Shows only active news for current school
    """
    queryset = News.objects.all()
    serializer_class = PublicNewsSerializer
    permission_classes = []  # No authentication
    pagination_class = None  # No pagination for public API
```

### Scenario 3: Admin-only Management View
```python
class ManagementView(SchoolScopedMixin, ListAPIView):
    """
    Admin view - sees all records including inactive
    """
    queryset = YourModel.objects.all()  # No IsActiveFilterMixin
    permission_classes = [IsAdminUser]
    return_all = True  # Superusers see all schools
```

### Scenario 4: Custom Filter Backend
```python
class CategoryFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category')
        if category:
            return queryset.filter(category__slug=category)
        return queryset

class ArticleListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    filter_backends = [CategoryFilterBackend, DjangoFilterBackend]
```

## 🚨 Security Checklist

### Before Deploying ANY Code:
- [ ] **Views use proper mixins**
  - [ ] `IsActiveFilterMixin` for public views
  - [ ] `SchoolScopedMixin` for school data
- [ ] **Admin classes use `SchoolAdminMixin`**
- [ ] **No manual school filtering** (use mixins instead)
- [ ] **Test with multiple schools**
- [ ] **Verify permission checks work**

### Testing Multi-tenancy:
```python
# Test template
def test_school_isolation(self):
    school1 = School.objects.create(name="School 1", domain="school1")
    school2 = School.objects.create(name="School 2", domain="school2")
    
    # Create data for school1
    obj1 = YourModel.objects.create(school=school1, name="Test 1")
    obj2 = YourModel.objects.create(school=school2, name="Test 2")
    
    # Test school1 subdomain
    self.client.defaults['HTTP_HOST'] = 'school1.example.com'
    response = self.client.get('/api/your-models/')
    
    # Should only see school1's data
    self.assertEqual(len(response.data['results']), 1)
    self.assertEqual(response.data['results'][0]['name'], "Test 1")
```

## 🎓 Learning Path

### Day 1: Understanding the Architecture
1. Read `PROJECT_ARCHITECTURE.md`
2. Explore `apps/common/mixins.py`
3. Study existing implementations in `apps/main/` and `apps/news/`

### Day 2: Hands-on Practice
1. Create a simple model with all mixins
2. Build views and admin interface
3. Test multi-tenant isolation

### Day 3: Advanced Patterns
1. Custom filter backends
2. Complex relationships
3. Translation management

### Week 1: Production Ready
1. Performance optimization
2. Advanced testing
3. Documentation

## 🔍 Debugging Tips

### Common Error Messages & Solutions

**"Forbidden for this tenant"**
```python
# Problem: Cross-tenant access
# Solution: Check SchoolScopedMixin configuration
class YourView(SchoolScopedMixin, ListAPIView):
    school_field = "school"  # Ensure this matches your FK field
```

**Empty results in views**
```python
# Problem: Missing school context
# Check middleware is running and subdomain is correct
def get_queryset(self):
    print(f"School: {self.request.school}")  # Debug
    return super().get_queryset()
```

**Admin shows all schools' data**
```python
# Problem: Missing SchoolAdminMixin
@admin.register(YourModel)
class YourModelAdmin(SchoolAdminMixin, admin.ModelAdmin):  # Add mixin
    pass
```

### Useful Debug Commands
```bash
# Check current migrations
python manage.py showmigrations

# Create translations
python manage.py makemessages -l uz -l ru -l en

# Test with specific host
curl -H "Host: school1.localhost:8000" http://localhost:8000/api/news/

# Check SQL queries
python manage.py shell
>>> from django.db import connection
>>> YourModel.objects.filter(school_id=1).query
```

## 📚 Essential Files to Know

1. **`apps/common/mixins.py`** - All reusable mixins
2. **`apps/common/models.py`** - BaseModel and managers
3. **`apps/main/middleware.py`** - Subdomain resolution
4. **`config/settings/base.py`** - Project configuration
5. **`apps/main/models.py`** - Core School model

## 🤝 Getting Help

1. **Check existing implementations** in `apps/main/` and `apps/news/`
2. **Read the mixins documentation** in `MIXINS_REFERENCE.md`
3. **Follow the established patterns** - don't reinvent the wheel
4. **Test thoroughly** with multiple schools
5. **Ask questions** if security implications are unclear

Remember: **When in doubt, follow the existing patterns!** 🎯 