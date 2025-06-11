from django.contrib import admin
from backend.lessons.models import Lesson, Task, UserTask

admin.site.register(Lesson)
admin.site.register(Task)
admin.site.register(UserTask)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title',)