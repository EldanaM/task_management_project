from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks-viewset', views.TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view()),
    path('tasks/my/', views.MyTasksView.as_view()),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view()),
    
    path('users/me/', views.CurrentUserView.as_view()),
    path('users/', views.UserListView.as_view()),
    
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('check-auth/', views.check_auth),
    
    path('', include(router.urls)),
]
