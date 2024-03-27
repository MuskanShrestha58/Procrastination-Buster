from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db.models import Avg
from django.urls import reverse
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    """
    Custom user model with additional attributes.

    Attributes:
        is_admin (bool): Indicates if the user is an admin (default False).
        is_user (bool): Indicates if the user is a regular user (default True).
    """
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)


class UserProfile(models.Model):
    """
    User profile model representing additional information about a user.

    Methods:
        task_completion_rate(): Calculate the completion rate of tasks for the user.
        goal_completion_rate(): Calculate the completion rate of goals for the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    total_tasks = models.PositiveIntegerField(default=0)
    total_goals = models.PositiveIntegerField(default=0)

    sex = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], null=True, blank=True)

    profession = models.CharField(max_length=255, null=True, blank=True)

    website_url = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)

    def task_completion_rate(self):
        """
        Calculate the completion rate of tasks for the user.

        Returns:
            float: Task completion rate as a percentage.
        """
        total_tasks = self.user.tasks.count()
        completed_tasks = self.user.tasks.filter(status='completed').count()
        if total_tasks == 0:
            return 0
        return (completed_tasks / total_tasks) * 100

    def goal_completion_rate(self):
        """
        Calculate the completion rate of goals for the user.

        Returns:
            float: Goal completion rate as a percentage.
        """
        total_goals = self.user.goals.count()
        completed_goals = self.user.goals.filter(progress=100).count()
        if total_goals == 0:
            return 0
        return (completed_goals / total_goals) * 100

    def __str__(self):
        return self.user.username


TASK_RATE_CHOICES = [
    (1, '1 - Mission Impossible'),
    (2, '2 - Fairly Tough'),
    (3, '3 - Just Right'),
    (4, '4 - Piece of Cake'),
    (5, '5 - Piece of Cake with a Cherry on Top'),
]

GOAL_RATE_CHOICES = [
    (1, '1 - Mildly Amazed'),
    (2, '2 - Happily Impressed'),
    (3, '3 - Smiling Ear to Ear'),
    (4, '4 - Dancing with Delight'),
    (5, '5 - On Cloud Nine'),
]


class Category(models.Model):
    name = models.CharField(max_length=350)
    # Default color is white
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [

        ('completed', 'Completed'),
        ('not completed', 'Not Completed'),
        ('dropped', 'Dropped'),
    ]

    title = models.CharField(max_length=350)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    favorites = models.ManyToManyField(
        UserProfile, related_name='favorite', default=None, blank=True)

    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    priority = models.IntegerField(
        choices=[
            (1, 'Low'),
            (2, 'Medium'),
            (3, 'High'),
            (4, 'Very High'),
            (5, 'Critical')
        ],
        default=3  # Default importance level
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    categories = models.ManyToManyField(
        Category, related_name='tasks', blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')

    start_date = models.DateTimeField(blank=True, null=True)
    collaborators = models.ManyToManyField(User, through='TaskCollaboration')
    """
    Get the absolute URL of the object.

    This method is used to retrieve the absolute URL of the object, which is often used in Django templates
    and views for generating links to the object's detail page.

    Returns:
        str: The absolute URL of the object.

    Example:
        If the object is a Goal instance with a primary key (pk) of 1 and the URL pattern for the goal detail view
        is defined as 'goal_detail', calling this method will return the URL '/goal_detail/1/'.
    """

    def get_absolute_url(self):
        return reverse('goal_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.title}"


class Goal(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    progress = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    categories = models.ManyToManyField(
        Category, related_name='goals', blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='goals')

    start_date = models.DateTimeField(blank=True, null=True)
    collaborators = models.ManyToManyField(
        User, related_name='collaborator_goals')
    priority = models.IntegerField(
        choices=[
            (1, 'Low'),
            (2, 'Medium'),
            (3, 'High'),
            (4, 'Very High'),
            (5, 'Critical')
        ],
        default=3  # Default importance level
    )

    def get_absolute_url(self):
        return reverse('goal_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.title}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, null=True, blank=True)

    def get_task_or_goal_url(self):
        if self.task:
            return self.task.get_absolute_url()
        elif self.goal:
            return self.goal.get_absolute_url()
        else:
            return None

    def __str__(self):
        return f"Notification to {self.recipient.username} at {self.timestamp}"


class TaskMemo(models.Model):
    DURING_TASK = 'during'
    AFTER_COMPLETION = 'after'
    MEMO_TYPES = [
        (DURING_TASK, 'During Task'),
        (AFTER_COMPLETION, 'After Completion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    memo_type = models.CharField(max_length=6, choices=MEMO_TYPES)
    task_rating = models.IntegerField(
        choices=TASK_RATE_CHOICES, blank=True, null=True)
    task_finish_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_memo_type_display()} Memo for {self.task} by {self.user}"


class GoalMemo(models.Model):
    DURING_TASK = 'during'
    AFTER_COMPLETION = 'after'
    MEMO_TYPES = [
        (DURING_TASK, 'During Task'),
        (AFTER_COMPLETION, 'After Completion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    memo_type = models.CharField(max_length=10, choices=MEMO_TYPES)
    satisfaction_level = models.IntegerField(
        choices=GOAL_RATE_CHOICES, blank=True, null=True)
    goal_finish_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_memo_type_display()} Memo for {self.goal} by {self.user}"


class TaskCollaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    # Additional fields specific to the collaboration relationship, if needed
    # For example, permissions, roles, etc.
    """
    Metadata options for the TaskCollaboration model.

    This class defines metadata options for the TaskCollaboration model. The 'unique_together' attribute
    specifies that each combination of 'user' and 'task' fields must be unique together, ensuring that
    a user cannot collaborate on the same task multiple times.

    Attributes:
        unique_together (tuple): A tuple specifying the combination of fields that must be unique together.
            In this case, it ensures that each user can collaborate on a task only once.
    """
    class Meta:
        unique_together = ('user', 'task')


class GoalCollaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    # Additional fields specific to the collaboration relationship, if needed
    # For example, permissions, roles, etc.

    class Meta:
        unique_together = ('user', 'goal')
# PACHI HALNE , GITHUB KO CONTRIBUTION JASTO WALA
    # class Award(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name


"""
    Signal receiver function that creates a corresponding UserProfile instance
    when a new User instance is created.

    Parameters:
        sender (class): The sender class of the signal.
        instance (object): The newly created User instance.
        created (bool): Indicates whether the User instance was created or not.
        kwargs (dict): Additional keyword arguments passed to the receiver.

    Returns:
        None
"""


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


"""
Connects the post_user_created_signal function as a receiver to the post_save signal
emitted by the User model. This ensures that the post_user_created_signal function
is called every time a User instance is saved (created or updated).
"""
post_save.connect(post_user_created_signal, sender=User)
