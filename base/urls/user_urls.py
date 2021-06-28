from django.urls import path
from base.views import user_views as views


urlpatterns = [
    path(
        "login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("register/",views.registerUser, name = 'register'),
    #path("distance/",views.getDistance, name = 'distance'),
    
    
    path("profile/", views.getUserProfile, name="user-profile"),
    
    path("profile/update/", views.updateUserProfile, name="user-profile-update"),
    
    path("upload/user", views.uploadUserImage, name="image-user-uplaod"),
    path("upload/farm", views.uploadFarmImage, name="image-farm-uplaod"),

    path("", views.getUsers, name="user"),
    
    path("<str:pk>/", views.getUserById, name="user"),
    path("update/<str:pk>/", views.updateUser, name="user-update"),

    path("delete/<str:pk>/", views.deleteUser, name="user-delete"),


    
]