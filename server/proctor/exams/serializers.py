from rest_framework import serializers
from exams.models import Exam


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('exam_id', 'exam_name', 'description', 'exam_date', 'start_at', 'end_at')
