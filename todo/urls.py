from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('subtasks/', views.SubTaskListView.as_view(), name='subtask-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('priorities/', views.PriorityListView.as_view(), name='priority-list'),
    path('notes/', views.NoteListView.as_view(), name='note-list'),
]