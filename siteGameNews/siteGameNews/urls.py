from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from homeblog.views import home_page, article_page, category_page, author_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home_page'),
    path('homeblog/<slug:slug>/', article_page, name='article_page'),
    path('homeblog/category/<slug:category>/', category_page, name='category_page'),
    path('homeblog/author/<slug:author>/', author_page, name='author_page')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

