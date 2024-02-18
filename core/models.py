from django.db import models

class Goal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    target_completion_date = models.DateField()
    difficulty = models.IntegerField(blank=True, null=True)
    associated_routines = models.ManyToManyField('Routine', blank=True)

    def __str__(self):
        return self.title

class Routine(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    associated_activities = models.ManyToManyField('Activity', blank=True)

    def __str__(self):
        return self.title

class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    estimated_duration = models.IntegerField()

    def __str__(self):
        return self.title
