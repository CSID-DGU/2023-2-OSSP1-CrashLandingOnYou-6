from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('signup/', views.sign_up_view, name='signup'),
    path('signin/', views.sign_in_view, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('myrecipe/<int:id>', views.myrecipe, name='mypage'),
    path('myrecipe/delete/<int:id>', views.myrecipe_delete, name='myrecipe-delete'),
    path('myrecipe/update/<int:id>', views.myrecipe_update, name='myrecipe-update'),
    path('myrecipe/update/end/<int:id>', views.myrecipe_update_end, name='myrecipe-update-end'),
]