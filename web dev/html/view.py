from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Activity, UserProgress

@login_required
def dashboard(request):
    # Fetch all activities and the user's progress for each activity
    activities = Activity.objects.all()
    user_progress = UserProgress.objects.filter(user=request.user)
    
    progress_data = {
        activity.id: user_progress.filter(activity=activity).first().progress if user_progress.filter(activity=activity).exists() else 0
        for activity in activities
    }

    return render(request, 'progress_app/dashboard.html', {
        'activities': activities,
        'progress_data': progress_data
    })

@login_required
def update_progress(request):
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        progress = int(request.POST.get('progress'))

        activity = Activity.objects.get(id=activity_id)
        user_progress, created = UserProgress.objects.get_or_create(user=request.user, activity=activity)

        # Update the progress
        user_progress.progress = progress
        user_progress.save()

        return JsonResponse({'progress': progress, 'message': 'Progress updated successfully.'})
    return JsonResponse({'message': 'Invalid request'}, status=400)
