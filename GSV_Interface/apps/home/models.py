# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    address = models.CharField(max_length=100)
    def __str__(self):
        return f"(self.address)"