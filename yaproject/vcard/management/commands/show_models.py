from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models
from django.conf import settings

import sys


class Command(BaseCommand):
    exclude_apps = ('django_coverage', 'staticfiles', 'messages')

    def handle(self, *args, **kwargs):
        for app_path in settings.INSTALLED_APPS:
            app_name = app_path.split('.')[-1]
            if app_name not in self.exclude_apps:
                app = get_app(app_name)

                for model in get_models(app):
                    cnt = model.objects.count()
                    out = '%s(%d) ' % (model.__name__, cnt)
                    sys.stderr.write('[error]' + out + '\n')
