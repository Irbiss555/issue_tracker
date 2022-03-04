from django.urls import path

from django.contrib.auth.views import LogoutView

from accounts.views import RegisterView, LoginUserView, UserProfileView, UserListView, UserUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='create'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/update', UserUpdateView.as_view(), name='user_update'),
]
