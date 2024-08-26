# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your models here.

from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    name = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)


class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', '未开始'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('delayed', '延期'),
    ]

    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]

    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    name = models.CharField(max_length=255)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # 0.00 to 100.00
    owner = models.ManyToManyField(User, related_name='projects', blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    gpa = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


class Daily(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()

    class Meta:
        unique_together = ('user_profile', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Report by {self.user_profile.user.username} on {self.date}"


class DailyItem(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    daily = models.ForeignKey(Daily, on_delete=models.CASCADE, related_name='items')


class GPA(models.Model):
    id = models.AutoField(primary_key=True)  # 默认行为是自动增长
    item = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    value = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
