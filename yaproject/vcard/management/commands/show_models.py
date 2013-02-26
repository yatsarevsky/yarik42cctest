from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models
from django.conf import settings

from StringIO import StringIO

import sys


class Command(BaseCommand):
    exclude_apps = ('django_coverage', 'staticfiles', 'messages')

    def handle(self, *args, **kwargs):
        sys.stderr = StringIO()

        for app_path in settings.INSTALLED_APPS:
            app_name = app_path.split('.')[-1]
            if app_name not in self.exclude_apps:
                out = '[%s]\n' % app_name
                print out
                sys.stderr.write('error:\n')
                sys.stderr.write(out)
                app = get_app(app_name)

                for model in get_models(app):
                    cnt = model.objects.count()
                    out = '\t%s (%d)' % (model.__name__, cnt)
                    print out
                    sys.stderr.write(out)
