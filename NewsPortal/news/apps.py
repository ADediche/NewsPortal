from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from .tasks import mailing_news
        from .scheduler import mailing_scheduler

        mailing_scheduler.add_job(
            id='mailing news',
            func=mailing_news,
            trigger='interval',
            days = 7,
        )
        mailing_scheduler.start()
