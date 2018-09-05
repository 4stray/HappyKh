from logging import Handler


class DataBaseHandler(Handler):
    """
    Emits a record
    to database
    """
    def emit(self, record):
        from .models import DataBaseLog

        templog = DataBaseLog(message=record.getMessage())
        templog.save()

