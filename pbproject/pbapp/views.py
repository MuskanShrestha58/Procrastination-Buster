from django.db.models import Count
from collections import Counter
from django.views import generic
from typing import Any
import random
import json
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils import timezone
from .forms import (
    CustomUserCreationForm,
    TaskCreationForm
)

from .models import (
    User,
    UserProfile,
    Task,
    Goal,
    Category,
    TaskMemo,
    GoalMemo,
    TaskCollaboration,
    GoalCollaboration,
    Notification,
)
from django.contrib.auth import get_user_model
from django.core import serializers
import numpy as np
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.


User = get_user_model()


class SignupView(generic.CreateView):
    """
    View for user registration/signup.

    Inherits from Django's generic CreateView.

    Attributes:
        template_name (str): The template to render for the signup page.
        form_class (Form): The form class to use for user signup.
    """

    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


class HomeView(generic.TemplateView):
    template_name = "pbapp/home.html"


class UserProfileView(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = "pbapp/user_profile.html"
    context_object_name = "user_profile"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'pbapp/task_create.html'
    # Redirect to task list page after successful creation
    success_url = reverse_lazy('pbapp:pbapp-tasklist')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign current user to the task
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "pbapp/task_list.html"

    def get_queryset(self):
        # Filter the queryset to only include tasks for the current user
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "pbapp/task_detail.html"
