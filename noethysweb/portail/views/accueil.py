# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import datetime
from django.views.generic import TemplateView
from django.db.models import Q
from portail.views.base import CustomView
from portail.utils import utils_approbations
from individus.utils import utils_pieces_manquantes
from core.models import PortailMessage, Article, Inscription, Consommation


class Accueil(CustomView, TemplateView):
    template_name = "portail/accueil.html"
    menu_code = "portail_accueil"

    def get_context_data(self, **kwargs):
        context = super(Accueil, self).get_context_data(**kwargs)
        context['page_titre'] = "Accueil"

        # Pièces manquantes
        context['nbre_pieces_manquantes'] = len(utils_pieces_manquantes.Get_pieces_manquantes(famille=self.request.user.famille, only_invalides=True))

        # Messages non lus
        context['nbre_messages_non_lus'] = len(PortailMessage.objects.filter(famille=self.request.user.famille, utilisateur__isnull=False, date_lecture__isnull=True))

        # Approbations
        approbations_requises = utils_approbations.Get_approbations_requises(famille=self.request.user.famille)
        context['nbre_approbations_requises'] = approbations_requises["nbre_total"]

        # Récupération des activités de la famille
        conditions = Q(famille=self.request.user.famille) & (Q(date_fin__isnull=False) | Q(date_fin__gte=datetime.date.today()))
        inscriptions = Inscription.objects.select_related("activite").filter(conditions)
        activites = list({inscription.activite: True for inscription in inscriptions}.keys())

        # Articles
        conditions = Q(statut="publie") & Q(date_debut__lte=datetime.datetime.now()) & (Q(date_fin__isnull=True) | Q(date_fin__gte=datetime.datetime.now()))
        conditions &= (Q(public__in=("toutes", "presents", "presents_groupes")) | (Q(public="inscrits") & Q(activites__in=activites)))
        articles = Article.objects.select_related("image_article", "album", "auteur").filter(conditions).distinct().order_by("-date_debut")
        selection_articles = []
        for article in articles:
            # Filtre les présents si besoin
            if article.public in ("presents", "presents_groupes"):
                conditions = Q(inscription__famille=self.request.user.famille, date__gte=article.present_debut, date__lte=article.present_fin, etat__in=("reservation", "present"))
                if article.public == "presents":
                    conditions &= Q(activite__in=article.activites.all())
                if article.public == "presents_groupes":
                    conditions &= Q(groupe__in=article.groupes.all())
                valide = Consommation.objects.filter(conditions).exists()
            else:
                valide = True
            if valide:
                selection_articles.append(article)
        context['articles'] = selection_articles

        return context
