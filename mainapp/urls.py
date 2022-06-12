from django.urls import path

import mainapp.views
from authapp import views as authapp_views
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name='index'),
    path("news/", views.NewsPageView.as_view(), name='news'),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/detail", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDeleteView.as_view(), name="news_delete"),
    path("courses/", views.CoursesListView.as_view(), name="courses"),
    path("courses/<int:pk>/", views.CoursesDetailView.as_view(), name="courses_detail"),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),
    path("contacts/", views.ContactsPageView.as_view(), name='contacts'),
    path("doc_site/", views.DocSitePageView.as_view(), name='docsite'),
    path("login/", authapp_views.CustomLoginView.as_view(), name='login'),
    path("logs", views.LogsView.as_view(), name='logs'),
    path("logs_download", views.LogsDownloadView.as_view(), name='logs_download'),
]
