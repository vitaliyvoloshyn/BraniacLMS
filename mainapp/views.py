from multiprocessing import context
from urllib import request
from django.http import HttpRequest
from django.views.generic import TemplateView, ListView, DetailView
import json


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class NewsPageView(ListView):
    template_name = "mainapp/news.html"
    paginate_by = 3
    
    def get_queryset(self):
        
        with open('mainapp/templates/mainapp/news.json', 'r') as f:
            self.queryset = json.load(f)
        return self.queryset


class ShowNews(DetailView):
    template_name = "mainapp/selected_news.html"
    pk_url_kwarg = 'news_id'

    def get_object(self):
        with open('mainapp/templates/mainapp/news.json', 'r') as f:
            self.queryset = json.load(f)
        return self.queryset[self.kwargs.get(self.pk_url_kwarg) - 1]


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"
