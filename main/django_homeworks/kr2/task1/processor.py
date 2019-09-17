from .models import Note


def processor(request):
    return {'NOTES_AMOUNT': Note.objects.all().count()}
