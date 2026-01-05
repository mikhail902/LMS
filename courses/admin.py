from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Lesson)
class ProdAdmin(admin.ModelAdmin):
    list_display = ("title", "preview", "description")
    list_filter = ("title",)


@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "preview")
