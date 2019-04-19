# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip = models.PositiveIntegerField(validators=[MinValueValidator(10000), MaxValueValidator(999999)])
    web = models.CharField(max_length=256)

    def __unicode__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name