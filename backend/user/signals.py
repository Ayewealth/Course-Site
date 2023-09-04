from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import *

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_instructor:
            InstructorProfile.objects.create(user=instance)
        elif instance.is_student:
            StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_instructor:
        instance.instructorprofile.save()
    elif instance.is_student:
        instance.studentprofile.save()

@receiver(post_save, sender=CustomUser)
def assign_user_roles(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            student_group, _ = Group.objects.get_or_create(name='Student')
            student_group.user_set.add(instance)

        if instance.is_instructor:
            instructor_group, _ = Group.objects.get_or_create(name='Instructor')
            instructor_group.user_set.add(instance)