from django.contrib import admin
from backend.lessons.models import Lesson, Task

admin.site.register(Lesson)
admin.site.register(Task)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title',)