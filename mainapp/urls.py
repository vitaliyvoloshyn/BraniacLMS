from django.urls import path

from mainapp import views
from authapp import views as authapp_views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name='index'),
    path("news/", views.NewsPageView.as_view(), name='news'),
    path("news/<int:news_id>/", views.ShowNews.as_view(), name='selected_news'),
    path("courses/", views.CoursesPageView.as_view(), name='courses'),
    path("contacts/", views.ContactsPageView.as_view(), name='contacts'),
    path("doc_site/", views.DocSitePageView.as_view(), name='docsite'),
    path("login/", authapp_views.CustomLoginView.as_view(), name='login'),
]
