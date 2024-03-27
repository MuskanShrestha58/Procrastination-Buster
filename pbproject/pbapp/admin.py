from django.contrib import admin
from .models import User, UserProfile, Task, Goal, Category, TaskMemo, GoalMemo, TaskCollaboration, GoalCollaboration, Notification
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Goal)
admin.site.register(Category)
admin.site.register(TaskMemo)
admin.site.register(GoalMemo)
admin.site.register(TaskCollaboration)
admin.site.register(GoalCollaboration)
admin.site.register(Notification)
