from django.urls import path
from . views import (
    HomeView,
    TaskCreateView,
    TaskListView,
    TaskDetailView

)
app_name = "pbapp"

urlpatterns = [
    path('', HomeView.as_view(), name="pbapp-home"),
    path('taskcreate/', TaskCreateView.as_view(), name='pbapp-taskcreate'),
    path('tasklist/', TaskListView.as_view(), name='pbapp-tasklist'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='pbapp-task_detail'),
]
