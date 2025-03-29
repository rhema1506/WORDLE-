from django.core.management.base import BaseCommand
from game.models import WordList

class Command(BaseCommand):
    help = 'Load 5-letter words into the database'

    def handle(self, *args, **kwargs):
        # Update this path if you keep your file elsewhere
        word_file_path = os.path.join(settings.BASE_DIR, 'WordList.txt')

        
        try:
            with open(word_file_path, 'r') as file:
                words = file.read().splitlines()
                count = 0
                for word in words:
                    word = word.strip().lower()
                    if len(word) == 5 and word.isalpha():
                        obj, created = Word.objects.get_or_create(text=word)
                        if created:
                            count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} words!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {word_file_path}'))
