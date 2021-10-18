from django.urls import path, include 
from apps.users.views import RegisterView, LoginView, LogoutView, DashboardView, UsersListView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # users crud
    path('users/list', UsersListView.as_view(), name='users_list'),
    path('users/create', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:id>', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:id>', UserDeleteView.as_view(), name='user_delete'),
    
]