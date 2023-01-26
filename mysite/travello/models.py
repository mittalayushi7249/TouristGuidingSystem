# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Places(models.Model):
	Name = models.CharField(max_length=200)
	Type = models.CharField(max_length=200)
	City = models.CharField(max_length=200)
	Image = models.ImageField()
	Location = models.CharField(max_length=1000)
	Description = models.CharField(max_length=2000)
	Ratings = models.IntegerField()


	def __str__(self):
		return self.Name


class Comments(models.Model):
	UserID = models.ForeignKey(User,on_delete=models.CASCADE)
	PlaceID = models.ForeignKey(Places,on_delete=models.CASCADE)
	Message = models.CharField(max_length=1000)
	PositveNegative = models.IntegerField(default=1)

	

class Feedback(models.Model):
	UserID = models.ForeignKey(User,on_delete=models.CASCADE)
	Message = models.CharField(max_length=1000)





