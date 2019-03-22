from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.postgres import fields as postgres_fields


class Student(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    day_of_birth = models.DateField()

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return str(self)


class Teacher(models.Model):

    POSITIONS = (
        ('Professor', 'Professor'),
        ('Assistant professor', 'Assistant professor'),
        ('Graduate student', 'Graduate student'),
        ('Assistant', 'Assistant'),
    )

    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    position = models.CharField(max_length=128, choices=POSITIONS)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return str(self)


class Note(models.Model):

    note = models.IntegerField(default=0, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(10)
    ])
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name="notes", verbose_name='Student')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name="notes", verbose_name='Student')

    day = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.note} from {self.teacher} to {self.student}'

    def __repr__(self):
        return str(self)
