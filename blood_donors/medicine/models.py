from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=10)
    birthday = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=50,default="client")
    exp = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.scheduled_date} \n Status: {self.status}"


class MedicalTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    blood_group = models.CharField(max_length=10)
    hemoglobin_level = models.DecimalField(max_digits=5, decimal_places=2)  # poziom hemoglobiny (g/dL)
    platelet_count = models.IntegerField()  # liczba płytek krwi (tys./µL)
    white_blood_cell_count = models.DecimalField(max_digits=5, decimal_places=2)  # liczba białych krwinek (tys./µL)
    blood_pressure_systolic = models.IntegerField()  # ciśnienie skurczowe
    blood_pressure_diastolic = models.IntegerField()  # ciśnienie rozkurczowe
    heart_rate = models.IntegerField()  # tętno
    comments = models.TextField(blank=True, null=True)  # dodatkowe uwagi lub komentarze
    is_eligible = models.BooleanField(default=True)  # czy pacjent jest zakwalifikowany do oddania krwi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Test Result for {self.user.username} on {self.test_date}"