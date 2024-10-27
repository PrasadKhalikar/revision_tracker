from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TopicForm
from .models import Topic
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'tracker/home.html')

@login_required
def mark_completed(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    topic.completed_date = date.today()
    topic.completed = True
    topic.save()
    messages.success(request, 'Topic marked as completed!')
    return redirect('index')

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('index')
    else:
        form = TopicForm(instance=topic)

    return render(request, 'tracker/edit_topic.html', {'form': form})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)

    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted successfully!')
        return redirect('index')

    return render(request, 'tracker/delete_topic.html', {'topic': topic})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the new user
            messages.success(request, 'Registration successful!')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please check your details.')
    else:
        form = UserCreationForm()

    return render(request, 'tracker/register.html', {'form': form})

def fibonacci(n):
    fib_seq = [1, 1]
    while len(fib_seq) < n:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq

def get_fibonacci_dates(date_added):
    fib_seq = fibonacci(10)  # Get the first 10 Fibonacci numbers (adjust as needed)
    revision_dates = [date_added + timedelta(days=fib) for fib in fib_seq]
    return revision_dates


@login_required
def index(request):
    today = date.today()
    topics_for_today = []

    # Fetch topics for the current user that are either not completed or have an older completion date
    all_topics = Topic.objects.filter(user=request.user)

    for topic in all_topics:
        # Check if the topic was completed today
        if topic.completed_date == today:
            continue  # Skip showing topics completed today
        
        # Get the Fibonacci revision dates for this topic
        revision_dates = get_fibonacci_dates(topic.date_added)
        
        # If today is one of the revision dates, add it to today's list
        if today in revision_dates:
            topics_for_today.append(topic)

    # Display a message about today's revision topics
    if topics_for_today:
        messages.info(request, f"You have {len(topics_for_today)} topics due for revision today!")
    else:
        messages.info(request, "No topics due for revision today.")

    context = {'topics_for_today': topics_for_today,'today':today}
    return render(request, 'tracker/index.html', context)

@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            form.save()
            return redirect('index')
    else:
        form = TopicForm()
    return render(request, 'tracker/add_topic.html', {'form': form})

# views.py

def calculate_progress(user):
    all_topics = Topic.objects.filter(user=user).count()
    completed_topics = Topic.objects.filter(user=user, completed=True).count()

    # Today's date for calculating revision topics
    today = date.today()
    topics_needing_revision_today = Topic.objects.filter(user=user).filter(
        date_added__in=[
            topic.date_added for topic in Topic.objects.filter(user=user)
            if today in get_fibonacci_dates(topic.date_added)
        ]
    )

    daily_completed = topics_needing_revision_today.filter(completed=True, completed_date=today).count()
    daily_total = topics_needing_revision_today.count()

    # Calculate remaining topics for today
    remaining_topics_today = daily_total - daily_completed

    # Calculate percentage for both daily and overall progress
    overall_progress = (completed_topics / all_topics) * 100 if all_topics else 0
    daily_progress = (daily_completed / daily_total) * 100 if daily_total else 0

    return overall_progress, daily_progress, daily_completed, remaining_topics_today

@login_required
def progress(request):
    # Get user-specific progress data
    overall_progress, daily_progress, daily_completed, remaining_topics_today = calculate_progress(request.user)

    context = {
        'overall_progress': overall_progress,
        'daily_progress': daily_progress,
        'daily_completed': daily_completed,
        'remaining_topics_today': remaining_topics_today,
    }
    return render(request, 'tracker/progress.html', context)
