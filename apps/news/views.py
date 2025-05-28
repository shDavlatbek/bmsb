from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from rest_framework.compat import coreapi, coreschema
from django.utils.encoding import force_str
import warnings
from django.utils.safestring import mark_safe
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.news.models import News, Category
from apps.news.serializers.news import NewsListSerializer, NewsDetailSerializer, CategorySerializer


class CategorySlugFilterBackend(BaseFilterBackend):
    """
    Custom filter backend that allows filtering news by category slug.
    Usage: ?category_slug=science-news
    """
    
    
    def filter_queryset(self, request, queryset, view):
        category_slug = request.query_params.get('category_slug')
        if category_slug:
            return queryset.filter(category__slug=category_slug)
        return queryset
    
    def to_html(self, request, queryset, view):
        """
        Render the filter for the browsable API.
        """
        categories = Category.objects.filter(is_active=True).values('slug', 'name')
        category_options = ''.join([
            f'<option value="{cat["slug"]}">{cat["name"]}</option>'
            for cat in categories
        ])
        
        current_value = request.query_params.get('category_slug', '')
        
        return mark_safe(f'''
        <div class="form-group">
            <label for="category_slug">Category:</label>
            <select name="category_slug" class="form-control">
                <option value="">All Categories</option>
                {category_options}
            </select>
        </div>
        <script>
            document.querySelector('select[name="category_slug"]').value = '{current_value}';
        </script>
        ''')
    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        if coreapi is not None:
            warnings.warn('CoreAPI compatibility is deprecated and will be removed in DRF 3.17', RemovedInDRF317Warning)
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Category Slug',
                    description='Filter news by category slug'
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'category_slug',
                'required': False,
                'in': 'query',
                'description': 'Filter news by category slug',
                'schema': {
                    'type': 'string',
                },
            },
        ]
        

class CategoryListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    """List view for news categories"""
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = []
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class NewsListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    """List view for news with filtering and search"""
    
    serializer_class = NewsListSerializer
    queryset = News.objects.all()
    permission_classes = []
    filter_backends = [
        DjangoFilterBackend,
        CategorySlugFilterBackend
    ]
    

class NewsDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    """Detail view for news with view count increment"""
    
    serializer_class = NewsDetailSerializer
    queryset = News.objects.all()
    permission_classes = []
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count when news is viewed
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
