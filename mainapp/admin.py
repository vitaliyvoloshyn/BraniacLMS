from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created', 'updated', 'deleted']
    search_fields = ['title', 'body']
    list_filter = ['created']


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'cost', 'deleted']
    ordering = ('cost',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk', "get_course_name", 'num', 'title', 'deleted']
    ordering = ("-course__name", '-num')
    list_per_page = 10
    list_filter = ["course", "created", "deleted"]
    actions = ['mark_deleted']

    def get_course_name(self, obj):
        return obj.course.name

    get_course_name.short_description = _("course")

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _("Mark deleted")


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ['name_first', 'name_second', 'day_birth', "get_course_name"]

    def get_course_name(self, obj):
        return list(obj.course.values_list('name', flat=True))

    get_course_name.short_description = _("course")


@admin.register(CourseFeedback)
class CourseFeedbackAdmin(admin.ModelAdmin):
    pass
