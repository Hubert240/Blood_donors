from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from .models import Profile, Reservation
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserEditForm, ProfileEditForm, ReservationForm, \
    MedicalTestResultForm


# Create your views here.


def home(request):
    return render(request, 'home.html')


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


def add_medical_test_result(request):
    if request.method == 'POST':
        form = MedicalTestResultForm(request.POST)
        if form.is_valid():
            medical_test_result = form.save(commit=False)
            medical_test_result.user = form.cleaned_data['user']
            medical_test_result.save()
            return redirect('medical_test_result_success')
    else:
        form = MedicalTestResultForm()
    return render(request, 'add_medical_test_result.html', {'form': form})