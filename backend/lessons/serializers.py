from rest_framework import serializers
from backend.lessons.models import (
    Lessons,
    LearningPaths,
    UserLearningProgress
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'


class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPaths
        fields = '__all__'


class UserLearningProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningProgress
        fields = '__all__'