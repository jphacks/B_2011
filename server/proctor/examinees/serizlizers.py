from rest_framework import serializers
from examinees.models import Examinee


class ExamineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examinee
        fields = ('examinee_id',)
