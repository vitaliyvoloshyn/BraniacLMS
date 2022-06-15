import logging

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, FileResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin

from BraniacLMS import settings
from mainapp import forms as mainapp_forms
from mainapp import tasks as mainapp_tasks
from mainapp.forms import CourseFeedbackForm
from mainapp.models import *

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class NewsPageView(ListView):
    model = News
    template_name = "mainapp/news.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = []
        nlk = 'news_list'
        news_list_cached = cache.get(nlk)
        if news_list_cached:
            queryset = news_list_cached
        else:
            queryset = queryset.filter(deleted=False).order_by('-created')
            cache.set('news_list', queryset, timeout=3600)
        return queryset


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)


class NewsDetailView(DetailView):
    template_name = "mainapp/selected_news.html"
    model = News

    def get_queryset(self):
        nlk = 'news_list'
        news_list_cached = cache.get(nlk)
        if news_list_cached:
            SingleObjectMixin.queryset = news_list_cached
        else:
            SingleObjectMixin.queryset = self.model.objects.filter(deleted=False).order_by('-created')
            cache.set('news_list', SingleObjectMixin.queryset, timeout=3600)
        return SingleObjectMixin.queryset

    def get_object(self, queryset=None):
        obj = None
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = cache.get(f"obj{pk}")
        if obj:
            return obj
        else:
            queryset = self.get_queryset()
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
            cache.set(f"obj{pk}", obj, timeout=3600)
        return obj


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)


class CoursesListView(ListView):
    template_name = "mainapp/courses_list.html"
    model = Courses
    paginate_by = 9


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"
    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Courses, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeachers.objects.filter(course=context["course_object"])
        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(course=context["course_object"], user=self.request.user).count():
                context["feedback_form"] = CourseFeedbackForm(course=context["course_object"], user=self.request.user)
        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = CourseFeedback.objects.filter(course=context["course_object"]).order_by(
                "-created", "-rating")[:5]
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)  # 5 minutes
        else:
            context["feedback_list"] = cached_feedback
        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(
                f"mail_feedback_lock_{self.request.user.pk}"
            )
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=300,
                )
                messages.add_message(
                    self.request, messages.INFO, _("Message sended")
                )
                mainapp_tasks.send_feedback_mail(
                    {
                        "user_id": self.request.POST.get("user_id"),
                        "message": self.request.POST.get("message"),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class SendMailPageView(TemplateView):
    template_name = "mainapp/send_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_staff:
            context["form"] = mainapp_forms.SendMailForm()
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_staff:
            res = send_mail(
                subject=self.request.POST.get('subject'),
                message=self.request.POST.get('message'),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.request.POST.get('to')],
                fail_silently=False
            )
            if res:
                messages.add_message(
                    self.request, messages.INFO, _("Message sent successfully")
                )
            else:
                messages.error(
                    self.request, _("Error")
                )

        return HttpResponseRedirect(reverse_lazy("mainapp:send_mail"))


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class LogsView(UserPassesTestMixin, TemplateView):
    template_name = "mainapp/logs_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logs_list = []

        # вывод первых 1000 лог-сообщений
        # with open(settings.LOG_FILE, 'r') as f:
        #     for i, line in enumerate(f.readlines()):
        #         if i == 1000:
        #             break
        #         logs_list.insert(0, line)

        # вывод последних (свежих) 100 лог-сообщений
        with open(settings.LOG_FILE) as f:  # узнаем количество строк в файле
            for rows_count, line in enumerate(f.readlines()):
                pass
        with open(settings.LOG_FILE) as f:  # читаем построчно, но с определенной строки
            i = 100  # задаем количество выводимых строк
            for j, line in enumerate(f.readlines()):
                if (rows_count - j) < i:
                    logs_list.insert(0, line)

        context['logs'] = logs_list
        print(context['logs'])
        return context


class LogsDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))
