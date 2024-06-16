from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, MedicalTestResult
from .models import Reservation


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,label="Imię:")
    last_name = forms.CharField(max_length=30, required=True, label="Nazwisko:")
    email = forms.EmailField(max_length=30,required=False)
    username = forms.CharField(label='Nazwa użytkownika:')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email' ,'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika', max_length=150)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['blood_group', 'birthday']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['scheduled_date']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MedicalTestResultForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Użytkownik")

    class Meta:
        model = MedicalTestResult
        fields = [
            'user', 'blood_group', 'hemoglobin_level', 'platelet_count', 'white_blood_cell_count',
            'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'comments', 'is_eligible'
        ]