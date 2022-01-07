from django.urls import path

from account.views import RegistrationView, ActivationView, LoginView, LogOutView, ChangePasswordView, \
    ForgotPasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('forgot_password', ForgotPasswordView.as_view())
]
