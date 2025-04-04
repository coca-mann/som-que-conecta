from django.contrib import admin
from .models import Lessons, LearningPaths, UserLearningProgress


admin.site.register(LearningPaths)
admin.site.register(UserLearningProgress)


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
