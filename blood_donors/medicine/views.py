from django.shortcuts import render
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from .models import Profile, Reservation, MedicalTestResult
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserEditForm, ProfileEditForm, ReservationForm, \
    MedicalTestResultForm
from django.contrib import messages  # Import the messages framework


#skumulowane
levels = {
    0: 0,
    1:500,
    2:1500,
    3:3000,
    4:5000,
    5:7500,
    6:11000,
    7:14000,
    8:18000,
    9:25000,
    10:30000
}
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        last_reservation = None
        can_make_new_reservation = False
        try:
            current_profile = Profile.objects.get(user=current_user)
            reservations = Reservation.objects.filter(user=current_user).order_by('scheduled_date')
            reservations_completed = Reservation.objects.filter(user=current_user, status='completed').order_by('scheduled_date')
            reservation_pending = Reservation.objects.filter(user=current_user, status='pending')
            if reservations:
                last_reservation = reservations.last()
            if reservations_completed:
                last_completed_reservation = reservations_completed.last()
                today=timezone.now()
                scheduled_date = last_completed_reservation.scheduled_date
                delta = scheduled_date+timedelta(days=90)
                if today>=delta and not reservation_pending:
                    can_make_new_reservation = True
            current_exp = current_profile.exp
            for key, value in levels.items():
                if current_exp >= value :
                    continue
                else:
                    current_level = key-1
                    if current_level == 10:
                        next_level = None
                        experience_missing = None
                        progress = 100
                        current_level = None
                        experience_missing = None
                        current_progress = None
                        required_progress = None
                        progress_2 = 0
                    else:
                        next_level = key
                        experience_missing = levels[next_level]-current_exp
                        current_progress = levels[current_level]-current_exp
                        required_progress = levels[next_level]-levels[current_level]
                        progress = round((current_progress/required_progress)*100,0)
                        progress_2 = 100 - progress
                    break



            return render(request,'home.html',{"profile": current_profile, "reservations": reservations,
                                               "current_level": current_level,
                                               "next_level": next_level,
                                               "experience_missing": experience_missing,
                                               "current_progress": current_progress,
                                               "progress": progress, "progress_2": progress_2,
                                               "last_reservation": last_reservation,
                                               "can_reserve": can_make_new_reservation})
        except Profile.DoesNotExist:
            profile = None
            reservations = None

    return render(request, 'home.html')

def ranking(request):
    users = Profile.objects.all().order_by('-exp')[:10]

    return render(request, 'ranking.html', {'users': users})
def admin_home(request):
    return render(request, 'admin_home.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            user.first_name = first_name
            last_name = form.cleaned_data.get('last_name')
            user.last_name = last_name
            email = form.cleaned_data.get('email')
            user.email = email
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')
        return redirect('/')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('admin_home')
                return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')


def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile')  # Przekierowanie po zapisaniu zmian
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })



def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('/')
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form})


def reservation_history(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-scheduled_date')
    return render(request, 'reservation_history.html', {'reservations': reservations})


def reservation_history_user(request):
    current_user = request.user
    reservations = Reservation.objects.filter(user=current_user)
    return render(request, 'reservation_history_user.html', {"reservations": reservations})


def add_medical_test_result(request):
    if request.method == 'POST':
        form = MedicalTestResultForm(request.POST)
        if form.is_valid():
            medical_test_result = form.save(commit=False)
            medical_test_result.user = form.cleaned_data['user']
            medical_test_result.save()
            messages.success(request, 'Dodano wyniki badań')
            return redirect('add_medical_test_result')
    else:
        form = MedicalTestResultForm()
    return render(request, 'add_medical_test_result.html', {'form': form})


def admin_view_medical_tests(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users to the home page

    medical_tests = MedicalTestResult.objects.all().order_by('-test_date')
    return render(request, 'admin_view_medical_tests.html', {'medical_tests': medical_tests})