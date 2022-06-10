from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView

from mainapp.forms import CourseFeedbackForm
from mainapp.models import *


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class NewsPageView(ListView):
    model = News
    template_name = "mainapp/news.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(deleted=False).order_by('-created')
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
        queryset = super().get_queryset()
        queryset = queryset.filter(deleted=False).order_by('-created')
        return queryset


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
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Courses, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeachers.objects.filter(course=context["course_object"])
        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(user=self.request.user):
                if not CourseFeedback.objects.filter(course=context["course_object"], user=self.request.user).count():
                    context["feedback_form"] = CourseFeedbackForm(course=context["course_object"], user=self.request.user)
                context["feedback_list"] = CourseFeedback.objects.filter(course=context["course_object"]).order_by(
                        "-created", "-rating")[:5]
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


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"
