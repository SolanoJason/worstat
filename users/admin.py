from django.contrib import admin
from .models import Account, Contact
from courses.models import Review, Course, Episode, Section, Enrollment, Answer, Question
from django import forms

# Register your models here.
admin.site.register(Account)
admin.site.register(Review)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Enrollment)

class EpisodeAdminForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'].widget.attrs['readonly'] = True

class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeAdminForm

admin.site.register(Episode, EpisodeAdmin)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4 

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Contact)