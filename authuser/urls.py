from django.urls import path
from .import views

urlpatterns = [
    path('register',views.register.as_view()),
    path('register/verify',views.verifyuserregister.as_view()),
    path('logmeout',views.logoutuser.as_view()),
    path('login',views.logginuser.as_view()),
    path('generateResetToken',views.ForgotPassGen.as_view()),
    path('validateFPR/user=<email>/token=<slug:token>',views.VerifyUserTokenAndUpdate.as_view()),
    path('isauth',views.is_user_auth.as_view()),
    path('getusername',views.GetUsername.as_view()),
]
