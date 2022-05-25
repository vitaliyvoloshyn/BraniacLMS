from multiprocessing import context
from urllib import request
from django.http import HttpRequest
from django.views.generic import TemplateView, ListView, DetailView
import json

from mainapp.models import News


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class NewsPageView(ListView):
    model = News
    template_name = "mainapp/news.html"
    paginate_by = 3
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(deleted=False).order_by('-created')
        return queryset


class ShowNews(DetailView):
    template_name = "mainapp/selected_news.html"
    pk_url_kwarg = 'news_id'
    model = News

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(deleted=False).order_by('-created')
        return queryset


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"
