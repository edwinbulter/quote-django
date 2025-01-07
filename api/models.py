from django.db import models

# Create your models here.
class Quote(models.Model):
    quote_text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    likes = models.IntegerField()

    def __str__(self):
        return f'{self.id} - {self.quote_text} - {self.author} - {self.likes}'
