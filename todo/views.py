from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView

from .models import Task, SubTask, Category, Priority, Note


class HomePageView(ListView):
    """Dashboard: not really a list view of one model, but reuses
    ListView so get_context_data() can add the stats we need."""
    model = Task
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_tasks'] = Task.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()

        context['tasks_completed'] = Task.objects.filter(status='Completed').count()
        context['tasks_pending'] = Task.objects.filter(status='Pending').count()
        context['tasks_in_progress'] = Task.objects.filter(status='In Progress').count()

        today = timezone.now().date()
        context['tasks_created_this_month'] = Task.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        ).count()

        return context


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['title', 'deadline', 'status', 'category__name', 'priority__name']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'title'


class SubTaskListView(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(title__icontains=query))
        return qs

    def get_ordering(self):
        allowed = ['title', 'status', 'parent_task__title']
        sort_by = self.request.GET.get('sort_by')
        if sort_by in allowed:
            return sort_by
        return 'parent_task__title'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 5
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs


class PriorityListView(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 5
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs


class NoteListView(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 5
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(content__icontains=query))
        return qs