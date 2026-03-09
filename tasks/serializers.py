from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class TaskSerializer(serializers.ModelSerializer):
    created_by_email = serializers.ReadOnlyField(source='created_by.email')
    assigned_to_email = serializers.ReadOnlyField(source='assigned_to.email')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 
                  'created_by', 'created_by_email', 'assigned_to', 'assigned_to_email']
        read_only_fields = ['created_at', 'created_by']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request:
            return attrs
        
        user = request.user
        instance = self.instance

        if instance:
            old_status = instance.status
            new_status = attrs.get('status', old_status)

            if old_status in ['done', 'rejected'] and new_status != old_status:
                raise serializers.ValidationError(
                    "Нельзя изменить завершенную или отклоненную задачу."
                )

            if user.role == 'client' and 'status' in attrs:
                raise serializers.ValidationError("Client не может менять статус.")

            if new_status == 'approved' and user.role not in ['moderator', 'admin']:
                raise serializers.ValidationError(
                    "approved может ставить только moderator или admin."
                )

            if new_status == 'done':
                if instance.assigned_to != user:
                    raise serializers.ValidationError(
                        "done может ставить только assigned_to."
                    )

        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
