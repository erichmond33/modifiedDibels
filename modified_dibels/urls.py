"""modified_dibels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dibels_test import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name="home"),
    path("maze", views.mazeAdmin, name="mazeAdmin"),
    path("image", views.imageAdmin, name="imageAdmin"),
    path("mazeSubmission", views.mazeSubmission, name="mazeSubmission"),
    path("maze-test/<int:metadata_id>", views.mazeGeneration, name="mazeGeneration"),
    path("image-test/<int:metadata_id>", views.imageGeneration, name="imageGeneration"),
    path("imageSubmission", views.imageSubmission, name="imageSubmission"),
    path("done", views.done, name="done"),
    path("continue-testing", views.continueTesting, name="continueTesting"),
    path("guidelines", views.guidelines, name="guidelines"),
    path("gallery", views.gallery, name="gallery"),
    path("data", views.addData, name="data")



]
'''
    path("demo", views.home_demo, name="home_demo"),
    path("mazeAdmin_demo", views.mazeAdmin_demo, name="mazeAdmin_demo"),
    path("imageAdmin_demo", views.imageAdmin_demo, name="imageAdmin_demo"),
    path("mazeSubmission_demo", views.mazeSubmission_demo, name="mazeSubmission_demo"),
    path("mazeGeneration_demo/<int:metadata_id>", views.mazeGeneration_demo, name="mazeGeneration_demo"),
    path("imageGeneration_demo/<int:metadata_id>", views.imageGeneration_demo, name="imageGeneration_demo"),
    path("imageSubmission_demo", views.imageSubmission_demo, name="imageSubmission_demo"),
'''