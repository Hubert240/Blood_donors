from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('reservation_history/', views.reservation_history, name='reservation_history'),
    path('add_medical_test_result/', views.add_medical_test_result, name='add_medical_test_result'),
    path('reservation_history_user/', views.reservation_history_user, name='reservation_history_user'),
    path('admin_view_medical_tests/', views.admin_view_medical_tests, name='admin_view_medical_tests'),
    path('ranking/', views.ranking, name='ranking'),
]