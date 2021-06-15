# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.core.management.base import BaseCommand
from django.core.management import call_command
import io


class Command(BaseCommand):
    help = 'Import des valeurs par defaut dans la base'

    def handle(self, *args, **kwargs):
        nom_fichier = "core/static/defaut/core.json"
        # Fermeture de toutes les connexions à la base
        from django import db
        db.connections.close_all()

        # Restauration
        stream = io.StringIO()
        error_stream = io.StringIO()
        call_command('loaddata', nom_fichier, **{
            # 'stdout': stream,
            # 'stderr': error_stream,
            # 'ignore': True,
            # 'database': DEFAULT_DB_ALIAS,
            'verbosity': 3})
        stream.seek(0)
        result = stream.read()
        self.stdout.write(self.style.SUCCESS("Données par défaut installées"))
