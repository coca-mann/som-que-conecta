from django.contrib import admin
from backend.lessons.models import Lesson, Task, UserTask, TaskAditionalResource

admin.site.register(Lesson)
admin.site.register(Task)
admin.site.register(UserTask)

@admin.register(TaskAditionalResource)
class TaskAditionalResourceAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'type', 'description', 'get_resource_display')
    list_filter = ('type', 'task_id__lesson')
    search_fields = ('description', 'task_id__title', 'task_id__lesson__title')
    readonly_fields = ('id',)
    
    def get_resource_display(self, obj):
        if obj.type == 'LINK':
            return obj.resource_link
        return obj.resource.name if obj.resource else '-'
    get_resource_display.short_description = 'Recurso'

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('title',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title',)