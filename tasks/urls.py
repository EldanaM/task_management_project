from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view()),
    path('tasks/my/', views.MyTasksView.as_view()),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view()),
    
    path('users/me/', views.CurrentUserView.as_view()),
    path('users/', views.UserListView.as_view()),
    
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('check-auth/', views.check_auth),
]