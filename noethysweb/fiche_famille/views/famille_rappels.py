# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.urls import reverse_lazy, reverse
from core.views.mydatatableview import MyDatatable, columns, helpers
from core.views import crud
from core.models import Famille, Rappel
from fiche_famille.views.famille import Onglet
from core.utils import utils_dates, utils_texte, utils_preferences
from django.db.models import Q



class Page(Onglet):
    model = Rappel
    url_liste = "famille_rappels_liste"
    description_liste = "Voici ci-dessous la liste des lettres de rappel générées pour cette famille."
    objet_singulier = "une lettre de rappel"
    objet_pluriel = "des lettres de rappel"



class Liste(Page, crud.Liste):
    model = Rappel
    template_name = "fiche_famille/famille_pieces.html"

    def get_queryset(self):
        return Rappel.objects.select_related('lot').filter(Q(famille=self.Get_idfamille()) & self.Get_filtres("Q"))

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['box_titre'] = "Lettres de rappel"
        context['onglet_actif'] = "outils"
        context['impression_introduction'] = ""
        context['impression_conclusion'] = ""
        return context

    class datatable_class(MyDatatable):
        filtres = ['idrappel', 'date_edition', 'numero', 'date_reference', 'solde', 'date_min', 'date_max', 'lot__nom']

        actions = columns.TextColumn("Actions", sources=None, processor='Get_actions_speciales')
        solde = columns.TextColumn("Solde", sources=['solde'], processor='Get_solde')
        lot = columns.TextColumn("Lot", sources=['lot__nom'])

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ['idrappel', 'date_edition', 'numero', 'solde', 'date_max', 'lot']
            #hidden_columns = = ["idrappel"]
            processors = {
                'date_edition': helpers.format_date('%d/%m/%Y'),
                'date_max': helpers.format_date('%d/%m/%Y'),
            }
            ordering = ['date_edition']

        def Get_solde(self, instance, **kwargs):
            return utils_texte.Formate_montant(instance.solde)

        def Get_actions_speciales(self, instance, *args, **kwargs):
            html = [
                self.Create_bouton_imprimer(url=reverse("famille_voir_rappel", kwargs={"idfamille": instance.famille_id, "idrappel": instance.pk}), title="Imprimer ou envoyer par email la lettre de rappel"),
            ]
            return self.Create_boutons_actions(html)
