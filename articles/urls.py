from django.urls import path
from .views import (ArticleCreateView,ArticleListView,ArticleUpdateView,ArticleDeleteView, CustomLoginView,CustomListView,UserRegistration,contact_form_view,user_update_profile_view,article_detail, list_article_view,UserArticleView
)
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

app_name = 'articles'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='articles:article-list'), name='logout'),
    path('register/',UserRegistration.as_view(),name='register'),
    path('',ArticleListView.as_view(), name='article-list'),
    path('user/<str:username>',UserArticleView.as_view(), name='user-article-list'),
    path('articles/tag/<slug:tag_slug>/',list_article_view, name='article-tag-list'),
    path('article/<int:pk>/detail/',article_detail, name='article-detail'),
    path('article/create/',ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/',ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/',ArticleDeleteView.as_view(), name='article-delete'),
    path('articles/edit',CustomListView.as_view(), name='article-cutomize'),
    path('profile/<int:pk>/update/', user_update_profile_view, name='update-view')
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
