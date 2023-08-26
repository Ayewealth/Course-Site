from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Assign roles to users based on the is_instructor and is_student fields.'

    def handle(self, *args, **kwargs):
        student_group, _ = Group.objects.get_or_create(name='Student')
        instructor_group, _ = Group.objects.get_or_create(name='Instructor')

        for user in CustomUser.objects.all():
            if user.is_student:
                student_group.user_set.add(user)

            if user.is_instructor:
                instructor_group.user_set.add(user)

        self.stdout.write(self.style.SUCCESS('Roles assigned successfully.'))
