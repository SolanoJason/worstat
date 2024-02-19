from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from moviepy.editor import VideoFileClip
from datetime import timedelta

# Create your models here.

class Course(models.Model):

    class Level(models.TextChoices):
        BEGINNER = "BG", "Principiante"
        INTERMEDIATE = "IN", "Intermedio"
        ADVANCED = "AD", "Avanzado"

    title = models.CharField("Titulo", max_length=255)
    description = models.CharField("Descripcion", max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name="users", through='Enrollment')
    price = models.DecimalField("Precio", max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    level = models.CharField("Nivel", choices=Level.choices, max_length=2)
    published_date = models.DateField('Fecha de publicacion', default=timezone.now)
    picture = models.ImageField(verbose_name="Imagen", max_length=500, upload_to='users', null=True)
    preference = models.JSONField(default=dict, editable=False)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self) -> str:
        return f'{self.title}'

    def get_duration(self):
        sections = Section.objects.filter(course=self)
        total_duration = sum(section.get_duration() for section in sections)
        return total_duration

    def get_duration_display(self):
        seconds = self.get_duration()
        seconds_timedelta = timedelta(seconds=seconds)
        hours, remainder = divmod(seconds_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        formatted_duration = f"{hours:02} h {minutes:02} m"
        return formatted_duration

    def get_num_episodes(self):
        # Retorna el número de episodios relacionados con este curso
        return sum(section.episode_set.count() for section in self.section_set.all())

class Question(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE)
    question = models.CharField("Pregunta", max_length=1000)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self) -> str:
        return f'{self.course}: {self.question}'

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.CASCADE)
    answer = models.CharField("Respuesta", max_length=1000, blank=False)
    is_correct = models.BooleanField("Correcto", default=False)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

    def __str__(self) -> str:
        return f'{self.question}: {self.answer}'

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE)
    enrollment_date = models.DateField('Fecha de inscripcion', default=timezone.now)
    is_completed = models.BooleanField('Completado', default=False)
    
    class Meta:
        verbose_name = "Matricula"
        verbose_name_plural = "Matriculas"
        unique_together = ["user", "course"]

    def __str__(self) -> str:
        return f'{self.user} enrolled in {self.course}'

class Section(models.Model):
    title = models.CharField(verbose_name="titulo", max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="curso")
    order = models.PositiveSmallIntegerField("orden")

    def __str__(self) -> str:
        return f'{self.course}: {self.title}'

    def get_duration(self):
        # get the duration of all the episodes in this section
        episodes = Episode.objects.filter(section=self)
        total_duration = sum(episode.duration for episode in episodes)
        return total_duration

    def get_duration_display(self):
        seconds = self.get_duration()
        seconds_timedelta = timedelta(seconds=seconds)
        hours, remainder = divmod(seconds_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        formatted_duration = f"{hours:02} h {minutes:02} m"
        return formatted_duration

    class Meta:
        ordering = ['order']
        verbose_name = "Seccion"
        verbose_name_plural = "Secciones"

def get_upload_to(instance, filename):
    return f'{instance.section.course.title}/{instance.section.title}/{instance.order}-{filename}'

def get_upload_file_to(instance, filename):
    return f'{instance.section.course.title}/{instance.section.title}/{instance.order}-{filename}-file'

class Episode(models.Model):

    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField("Orden")
    video = models.FileField('Video', upload_to=get_upload_to, max_length=500)
    duration = models.PositiveIntegerField("Duracion", default=0)
    free = models.BooleanField("Gratis", default=False)
    file = models.FileField("Archivo", upload_to=get_upload_file_to, max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.section}:{self.order}-{self.title}'

    def get_duration(self):
        try:
            with VideoFileClip(self.video.path) as video:
                duration = int(video.duration)
                return duration
        except Exception as e:
            print(f"Error calculating duration for {self.title}: {e}")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Clase"
        verbose_name_plural = "Clases"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE)
    comment = models.TextField("Comentario")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    # rating = models.PositiveSmallIntegerField("Calificacion", validators=[MaxValueValidator(5)], default=1)

    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'

    def __str__(self) -> str:
        return f'{self.comment}'

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='course', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField("transaction date", auto_now=True)
    amount = models.DecimalField("amount", max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f'Transaction on {self.course} by {self.user}: S/{self.amount}'

