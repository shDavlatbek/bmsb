from django.contrib import admin
from utils.admin import AdminTranslation

from . import models


class NewsAdmin(AdminTranslation):
    list_display = ("title", "created_at", "updated_at")


admin.site.register(models.News, NewsAdmin)