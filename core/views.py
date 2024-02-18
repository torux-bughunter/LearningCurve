from datetime import datetime, timedelta
from django.db.models import *
from django.db.models.functions import *
from django.http import JsonResponse

from django.shortcuts import render, redirect
from .models import Goal, Routine


def goals_list(request):
    goals = Goal.objects.all()
    return render(request, 'core/goals_list.html', {'goals': goals})


def create_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        target_completion_date = request.POST.get('target_completion_date')
        difficulty = request.POST.get('difficulty')

        goal = Goal.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            target_completion_date=target_completion_date,
            difficulty=difficulty
        )
        return redirect('calendar')
    return render(request, 'core/create_goal.html')


def goal_detail(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    return render(request, 'core/goal_detail.html', {'goal': goal})


def create_routine(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time_str = request.POST.get('start_time')
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M')
        except ValueError:
            # Handle invalid time format
            pass
        end_time_str = request.POST.get('end_time')
        try:
            end_time = datetime.strptime(end_time_str, '%H:%M')
        except ValueError:
            # Handle invalid time format
            pass

        routine = Routine.objects.create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return redirect('calendar')
    return render(request, 'core/create_routine.html')


from datetime import datetime, timedelta
from .models import Goal, Routine
from django.shortcuts import render


def calendar(request):
    # Retrieve all goals and routines
    goals = Goal.objects.all()
    routines = Routine.objects.all()

    # Create a dictionary to store events for each day
    calendar = {}

    # Get today's date
    today = datetime.now().date()

    # Iterate over the next 7 days including today
    for i in range(8):
        date = today + timedelta(days=i)
        calendar[date] = {'goals': [], 'routines': []}

        # Filter goals for the current date
        goals_for_date = goals.filter(target_completion_date=date)
        for goal in goals_for_date:
            event = {'type': 'goal', 'event': goal}
            calendar[date]['goals'].append(event)

        # Filter routines for the current date
        routines_for_date = routines.filter(start_time__date=date)
        for routine in routines_for_date:
            event = {'type': 'routine', 'event': routine}
            calendar[date]['routines'].append(event)

    return render(request, 'core/calendar.html', {'calendar': calendar})


def process_braindump(request):
    if request.method == 'POST':
        # Extract braindump from POST data
        braindump = request.POST.get('braindump', '')

        # Compile tasks from the braindump
        tasks = compile_tasks(braindump)

        # Save tasks to the calendar
        for task in tasks:
            # Here you would add the logic to save tasks to your database or calendar
            # For example, creating a new Goal object for each task
            # You can adjust this part based on your actual data model
            goal = Goal.objects.create(
                title=task,
                description='Braindump task',
                start_date=datetime.now().date(),
                target_completion_date=datetime.now().date(),
                # Example: set target completion date to 7 days from now
                difficulty=5  # Example: set difficulty level
            )

        # Return success response
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def compile_tasks(braindump):
    tasks = []
    lines = braindump.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            tasks.append(line)
    return tasks
