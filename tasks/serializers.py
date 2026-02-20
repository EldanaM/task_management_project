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
        fields = ['id', 'title', 'description', 'status', 'created_at', 'created_by', 'created_by_email', 'assigned_to', 'assigned_to_email']
        read_only_fields = ['created_at', 'created_by']
    
    def validate(self, data):
        request = self.context.get('request')
        if not request:
            return data
        
        user = request.user
        task = self.instance
        
        if 'status' in data:
            new_status = data['status']
            
            if task and task.status in ['done', 'rejected']:
                raise serializers.ValidationError('Нельзя менять выполненную или отклоненную задачу')
            
            if user.role == 'client':
                raise serializers.ValidationError('Клиент не может менять статус')
            
            if new_status == 'approved' and user.role != 'moderator':
                raise serializers.ValidationError('Только модератор может одобрять задачи')
            
            if new_status == 'done':
                if not task or task.assigned_to != user:
                    raise serializers.ValidationError('Только исполнитель может отметить как выполненное')
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)