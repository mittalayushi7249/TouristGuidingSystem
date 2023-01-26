# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Places)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass

