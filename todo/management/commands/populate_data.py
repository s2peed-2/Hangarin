import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from todo.models import Priority, Category, Task, SubTask, Note

fake = Faker()

PRIORITY_NAMES = ["High", "Medium", "Low", "Critical", "Optional"]
CATEGORY_NAMES = ["Work", "School", "Personal", "Finance", "Projects"]
STATUS_VALUES = ["Pending", "In Progress", "Completed"]


class Command(BaseCommand):
    help = (
        "Seeds the database: Priority and Category are added manually, "
        "then Task, SubTask, and Note records are generated with Faker."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--tasks",
            type=int,
            default=30,
            help="How many Task records to generate (default: 30).",
        )

    def handle(self, *args, **options):
        num_tasks = options["tasks"]

        priorities = self._seed_priorities()
        categories = self._seed_categories()
        tasks = self._seed_tasks(num_tasks, priorities, categories)
        self._seed_subtasks(tasks)
        self._seed_notes(tasks)

        self.stdout.write(self.style.SUCCESS(
            f"Done. {Priority.objects.count()} priorities, "
            f"{Category.objects.count()} categories, "
            f"{Task.objects.count()} tasks, "
            f"{SubTask.objects.count()} subtasks, "
            f"{Note.objects.count()} notes."
        ))

    def _seed_priorities(self):
        priorities = []
        for name in PRIORITY_NAMES:
            obj, created = Priority.objects.get_or_create(name=name)
            priorities.append(obj)
            if created:
                self.stdout.write(f"Added priority: {name}")
        return priorities

    def _seed_categories(self):
        categories = []
        for name in CATEGORY_NAMES:
            obj, created = Category.objects.get_or_create(name=name)
            categories.append(obj)
            if created:
                self.stdout.write(f"Added category: {name}")
        return categories

    def _seed_tasks(self, num_tasks, priorities, categories):
        tasks = []
        for _ in range(num_tasks):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=STATUS_VALUES),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
            tasks.append(task)
        self.stdout.write(f"Created {len(tasks)} tasks.")
        return tasks

    def _seed_subtasks(self, tasks):
        count = 0
        for task in tasks:
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=5),
                    status=fake.random_element(elements=STATUS_VALUES),
                )
                count += 1
        self.stdout.write(f"Created {count} subtasks.")

    def _seed_notes(self, tasks):
        count = 0
        for task in tasks:
            for _ in range(random.randint(0, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )
                count += 1
        self.stdout.write(f"Created {count} notes.")
