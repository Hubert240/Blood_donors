from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, MedicalTestResult, Reservation


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Imię:")
    last_name = forms.CharField(max_length=30, required=True, label="Nazwisko:")
    email = forms.EmailField(max_length=30, required=False)
    username = forms.CharField(label='Nazwa użytkownika:')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


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
        labels = {
            'blood_group': 'Grupa krwi',
            'hemoglobin_level': 'Poziom hemoglobiny',
            'platelet_count': 'Liczba płytek krwi',
            'white_blood_cell_count': 'Liczba białych krwinek',
            'blood_pressure_systolic': 'Ciśnienie skurczowe',
            'blood_pressure_diastolic': 'Ciśnienie rozkurczowe',
            'heart_rate': 'Tętno',
            'comments': 'Komentarze',
            'is_eligible': 'Czy kwalifikowany'
        }


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['status']
        labels = {
            'status': 'Status',
        }
        widgets = {
            'status': forms.Select(choices=[
                ('pending', 'Pending'),
                ('confirmed', 'Confirmed'),
                ('completed', 'Completed'),
                ('cancelled', 'Cancelled')
            ])
        }