from django.shortcuts import redirect

from .models import Note

class Task1Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        if Note.objects.filter(is_sold=True).count() == 0 and not \
                request.path.startswith('/admin') and not \
                request.path.startswith('/message'):
            return redirect('note_not')

        return self.get_response(request)
