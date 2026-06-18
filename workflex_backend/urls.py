from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('bid/<int:bid_id>/<str:action>/', views.update_bid_status, name='update_bid_status'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bids/', views.my_bids, name='my_bids'),
    path('my-projects/', views.my_projects, name='my_projects'),
]