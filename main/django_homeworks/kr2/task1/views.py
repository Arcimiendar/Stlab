from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView, TemplateView

from .models import Teacher, Student, Note


class MainPageView(View):

    def get(self, request):
        context = {
            'students': Student.objects.all(),
            'teachers': Teacher.objects.all(),
        }

        return render(request, 'task1/main.html', context=context)


class StudentDeleteView(DeleteView):

    model = Student
    template_name = 'task1/delete.html'
    success_url = reverse_lazy('main')


class TeacherDeleteView(DeleteView):

    model = Teacher
    template_name = 'task1/delete.html'
    success_url = reverse_lazy('main')


class StudentCreateView(CreateView):

    model = Student
    template_name = 'task1/create.html'
    success_url = reverse_lazy('main')
    fields = ('name', 'surname', 'day_of_birth')


class TeacherCreateView(CreateView):

    model = Teacher
    template_name = 'task1/create.html'
    success_url = reverse_lazy('main')
    fields = ('name', 'surname', 'position')


class StudentEditView(UpdateView):

    model = Student
    template_name = 'task1/create.html'
    success_url = reverse_lazy('main')
    fields = ('name', 'surname', 'day_of_birth')


class TeacherEditView(UpdateView):

    model = Teacher
    template_name = 'task1/create.html'
    success_url = reverse_lazy('main')
    fields = ('name', 'surname', 'position')


class StudentDetailView(DetailView):

    model = Student
    template_name = 'task1/detail_student.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        context['notes'] = list(Note.objects.filter(student=self.object).all())

        return context


class TeacherDetailView(DetailView):

    model = Teacher
    template_name = 'task1/detail_teacher.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        context['notes'] = list(Note.objects.filter(teacher=self.object).all())

        return context


class NoteCreateTeacherView(CreateView):

    model = Note
    template_name = 'task1/create.html'
    fields = ('note', 'student')
    success_url = reverse_lazy('main')

    def form_valid(self, form):



        self.object = Note(
            teacher_id=self.kwargs['pk'], **form.cleaned_data
        )

        self.object.save()

        return redirect(f'/teachers/{self.object.teacher_id}')



class NoteCreateStudentView(CreateView):

    model = Note
    template_name = 'task1/create.html'
    fields = ('note', 'student')
    success_url = reverse_lazy('main')

    def form_valid(self, form):

        self.object = Note(
            teacher_id=self.kwargs['pk'], **form.cleaned_data
        )

        self.object.save()

        return redirect(f'/students/{self.object.student_id}')


class MessageView(TemplateView):

    template_name = 'task1/message.html'
