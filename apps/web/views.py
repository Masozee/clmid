from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    pass
#calendar    
web_home_view = HomeView.as_view(template_name="frontend/index.html")
