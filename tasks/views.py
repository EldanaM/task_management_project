from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.all()
        
        if user.role == 'client':
            tasks = tasks.filter(Q(created_by=user) | Q(assigned_to=user))
        
        status = self.request.query_params.get('status')
        if status:
            tasks = tasks.filter(status=status)
        
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at']:
            tasks = tasks.order_by(ordering)
        
        return tasks
    
    def perform_create(self, serializer):
        serializer.save()

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        user = request.user
        
        if request.method == 'DELETE':
            if user.role != 'admin':
                self.permission_denied(request, 'Только админ может удалять')
        
        if user.role == 'client':
            if obj.created_by != user and obj.assigned_to != user:
                self.permission_denied(request, 'Это не ваша задача')

class MyTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(created_by=user) | Q(assigned_to=user))

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email и пароль обязательны'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'id': user.id,
            'email': user.email,
            'role': user.role
        })
    else:
        return Response(
            {'error': 'Неверный email или пароль'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Выход выполнен'})

@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    if request.user.is_authenticated:
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'role': request.user.role
        })
    return Response({'error': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)