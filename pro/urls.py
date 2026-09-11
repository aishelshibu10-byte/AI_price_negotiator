from django.contrib import admin
from django.urls import path
from jet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_list, name='product_list'),
]