"""kr2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from task1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainPageView.as_view(), name='main'),
    path('students/<int:pk>/delete', views.StudentDeleteView.as_view()),
    path('teachers/<int:pk>/delete', views.TeacherDeleteView.as_view()),
    path('students/<int:pk>/edit', views.StudentEditView.as_view()),
    path('teachers/<int:pk>/edit', views.TeacherEditView.as_view()),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='student'),
    path('teachers/<int:pk>', views.TeacherDetailView.as_view(), name='teacher'),
    path('students/create', views.StudentCreateView.as_view()),
    path('teachers/create', views.TeacherCreateView.as_view()),
    path('note/teacher/<int:pk>/create', views.NoteCreateTeacherView.as_view()),
    path('note/student/<int:pk>/create', views.NoteCreateStudentView.as_view()),
    path('message', views.MessageView.as_view()),
]
