from django.contrib import admin
from .models import WordList

@admin.register(WordList)
class WordListAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')
