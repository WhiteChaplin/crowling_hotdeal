from rest_framework import serializers
from .models import Deal

class DealSerializers(serializers.ModelSerializer):
    class Meta:
        model = Deal #DB에 저장된 내용을 데이터 모델로 사용
        fields = ('__all__') #모든 필드의 값 사용