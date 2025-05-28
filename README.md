# 🏫 BMSB - Multi-Tenant School Management System

[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![Multi-Language](https://img.shields.io/badge/Languages-UZ%20%7C%20RU%20%7C%20EN-orange.svg)]()

BMSB is a robust multi-tenant school management system that provides each school with its own subdomain-based workspace. Built with Django and Django REST Framework, it features comprehensive school management tools, content management, news systems, and multi-language support.

## ✨ Key Features

### 🏗️ **Multi-Tenant Architecture**
- **Subdomain-based isolation**: Each school gets `schoolname.yourdomain.com`
- **Secure data separation**: Complete isolation between schools
- **Shared infrastructure**: Cost-effective hosting for multiple schools

### 🌍 **Internationalization**
- **Multi-language support**: Uzbek (default), Russian, English
- **Admin translation interface**: Tabbed editing for all languages
- **Content localization**: Automatic language detection and fallbacks

### 📚 **Content Management**
- **Rich text editing**: TinyMCE integration with image management
- **News & announcements**: Categorized content system
- **Media management**: Automatic image optimization and organized uploads
- **Menu system**: Hierarchical navigation with MPTT

### 🔐 **Security & Permissions**
- **Role-based access**: Superusers, school admins, and users
- **Tenant isolation**: Automatic school-scoped data access
- **Active record filtering**: Soft deletion with public/admin visibility control
- **Permission layers**: Multiple security checkpoints

### ⚡ **Developer Experience**
- **Reusable mixins**: Standardized patterns for security and functionality
- **Code templates**: Quick-start templates for new features
- **Comprehensive documentation**: Architecture guides and API references
- **Testing utilities**: Multi-tenant testing helpers

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.10+
- Django 5.2+
- PostgreSQL (production) or SQLite (development)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd bmsb

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements/base.txt

# Environment setup
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### First Steps
1. Visit `http://localhost:8000/admin/` and log in as superuser
2. Create your first school in the admin
3. Set up subdomain (e.g., add `127.0.0.1 testschool.localhost` to `/etc/hosts`)
4. Visit `http://testschool.localhost:8000/` to see the school's site

## 🏗️ Architecture Overview

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   school1.domain    │    │   school2.domain    │    │   school3.domain    │
│                     │    │                     │    │                     │
│   School 1 Data     │    │   School 2 Data     │    │   School 3 Data     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           └───────────────────────────┼───────────────────────────┘
                                       │
                              ┌─────────────────────┐
                              │   Shared Platform   │
                              │                     │
                              │  • User Management  │
                              │  • Content Engine   │
                              │  • Admin Interface  │
                              │  • API Framework    │
                              └─────────────────────┘
```

### Core Components

#### **Apps Structure**
- **`apps/common/`** - Shared utilities, mixins, and base models
- **`apps/main/`** - Core school functionality and models
- **`apps/news/`** - News and announcement system
- **`apps/media/`** - Media management and file handling
- **`apps/user/`** - User management and authentication
- **`apps/resource/`** - Educational resources and materials

#### **Multi-Tenant Flow**
1. **Request arrives** → `SubdomainMiddleware` extracts school from subdomain
2. **School resolution** → Middleware sets `request.school` context
3. **View processing** → Mixins automatically filter data by school
4. **Data isolation** → Only current school's data is accessible

## 🧩 Core Mixins

### View Mixins
- **`IsActiveFilterMixin`** - Filters inactive records from public APIs
- **`SchoolScopedMixin`** - Provides automatic school-based data isolation
- **`ActiveModelMixin`** - Simple active-only filtering for views

### Admin Mixins
- **`SchoolAdminMixin`** - Multi-tenant admin with school-scoped data
- **`AdminTranslation`** - Tabbed translation interface
- **`DescriptionMixin`** - Enhanced rich text field handling

### Model Mixins
- **`SlugifyMixin`** - Automatic slug generation from source fields
- **`BaseModel`** - Timestamps, soft deletion, and custom managers

## 📖 Documentation

### For Developers
- **[📋 Project Architecture](PROJECT_ARCHITECTURE.md)** - Complete system overview
- **[🧩 Mixins Reference](MIXINS_REFERENCE.md)** - Detailed mixin documentation
- **[🚀 Quick Start Guide](DEVELOPER_QUICKSTART.md)** - Templates and patterns

### Key Concepts
- **Multi-tenancy**: Subdomain-based school isolation
- **Security mixins**: Automatic data filtering and permission checks
- **Translation system**: Multi-language content management
- **Soft deletion**: `is_active` field with public/admin visibility

## 🔧 Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# TinyMCE (optional)
TINYMCE_API_KEY=your-tinymce-api-key
```

### Language Settings
```python
# config/settings/base.py
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')
LANGUAGE_CODE = 'uz'
LANGUAGES = [
    ('uz', 'Uzbek'),
    ('en', 'English'),
    ('ru', 'Russian'),
]
```

### Multi-tenant Configuration
```python
# Middleware order is important
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'apps.main.middleware.SubdomainMiddleware',  # Must be early
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middleware
]
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.news

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Multi-tenant Testing Pattern
```python
class MultiTenantTestCase(TestCase):
    def setUp(self):
        self.school1 = School.objects.create(name="School 1", domain="school1")
        self.school2 = School.objects.create(name="School 2", domain="school2")
    
    def test_data_isolation(self):
        # Test that schools can't access each other's data
        self.client.defaults['HTTP_HOST'] = 'school1.example.com'
        # ... test assertions
```

## 🚀 Deployment

### Production Considerations
1. **Database**: Use PostgreSQL with proper indexing
2. **Media files**: Configure cloud storage (AWS S3, etc.)
3. **Subdomain setup**: Wildcard DNS configuration
4. **Security**: HTTPS, proper SECRET_KEY, security headers
5. **Performance**: Redis caching, database optimization

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f prod.yml up -d

# Or build manually
docker build -f Dockerfile .
```

## 🤝 Contributing

### Development Workflow
1. **Fork and clone** the repository
2. **Create feature branch** from `main`
3. **Follow established patterns** using project mixins
4. **Write tests** for new functionality
5. **Test multi-tenant isolation** thoroughly
6. **Submit pull request** with clear description

### Code Standards
- **Always use security mixins** for views and admin
- **Follow naming conventions** (Uzbek verbose names)
- **Write comprehensive tests** especially for multi-tenancy
- **Document new features** and update guides

### Security Requirements
- **Never bypass tenant isolation** without explicit approval
- **Always test with multiple schools** to verify isolation
- **Use proper mixins** instead of manual filtering
- **Validate permissions** at multiple layers

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
1. **Read the documentation** in this repository
2. **Check existing implementations** in `apps/main/` and `apps/news/`
3. **Follow established patterns** - don't reinvent solutions
4. **Test thoroughly** with multiple schools
5. **Ask questions** if security implications are unclear

### Common Issues
- **Empty API results**: Check subdomain middleware and school context
- **Cross-tenant data leakage**: Verify proper mixin usage
- **Admin permission issues**: Ensure `SchoolAdminMixin` is used
- **Translation problems**: Check translation registration and configuration

## 🎯 Roadmap

### Planned Features
- [ ] Advanced reporting and analytics
- [ ] Student and teacher management modules
- [ ] Class scheduling system
- [ ] Grade management
- [ ] Parent portal integration
- [ ] Mobile app API enhancements

### Performance Improvements
- [ ] Database query optimization
- [ ] Caching strategy implementation
- [ ] CDN integration for media files
- [ ] Background task processing

---

**Built with ❤️ for educational institutions**

*BMSB provides a scalable, secure, and feature-rich platform for modern school management.* 