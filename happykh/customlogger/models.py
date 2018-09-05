from django.db import models


class DataBaseLog(models.Model):
    """
    Fields:
    publishing_date - keeps a date when error was occurred
    message - keeps log's message
    """
    publishing_date = models.DateField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        ordering = ('-publishing_date',)
        app_label = 'customlogger'

    def __str__(self):
        return self.message
