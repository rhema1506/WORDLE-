import os
from django.core.management.base import BaseCommand
from django.conf import settings
from game.models import WordList, WordLength

class Command(BaseCommand):
    help = 'Load 4, 5, and 6-letter words into the database'

    def handle(self, *args, **kwargs):
        word_file_path = os.path.join(settings.BASE_DIR, 'WordList.txt')

        # Cache WordLength objects for lengths 4,5,6
        lengths = [4, 5, 6]
        length_objs = {length: WordLength.objects.get_or_create(length=length)[0] for length in lengths}

        try:
            with open(word_file_path, 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
                count = 0
                for word in words:
                    word = word.strip().lower()
                    if len(word) in lengths and word.isalpha():
                        wl_obj = length_objs[len(word)]
                        obj, created = WordList.objects.get_or_create(
                            word=word,
                            defaults={'language': 'en', 'word_length': wl_obj}
                        )
                        if created:
                            count += 1

                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} words of length 4, 5, and 6!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {word_file_path}'))
