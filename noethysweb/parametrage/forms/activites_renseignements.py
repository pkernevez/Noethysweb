# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from django.forms import ModelForm
from core.forms.base import FormulaireBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import Field
from core.utils.utils_commandes import Commandes
from core.models import Activite, TypePiece, TypeCotisation, TypeConsentement
from django_select2.forms import Select2MultipleWidget


class Formulaire(FormulaireBase, ModelForm):
    class Meta:
        model = Activite
        fields = ["pieces", "cotisations", "vaccins_obligatoires", "types_consentements"]
        widgets = {
            "pieces": Select2MultipleWidget({"lang": "fr", "data-width": "100%"}),
            "cotisations": Select2MultipleWidget({"lang": "fr", "data-width": "100%"}),
            "types_consentements": Select2MultipleWidget({"lang": "fr", "data-width": "100%"}),
         }

    def __init__(self, *args, **kwargs):
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'activites_renseignements_form'
        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        # Création des boutons de commande
        if self.mode == "CONSULTATION":
            commandes = Commandes(modifier_url="activites_renseignements_modifier", modifier_args="idactivite=activite.idactivite", modifier=True, enregistrer=False, annuler=False, ajouter=False)
            self.Set_mode_consultation()
        else:
            commandes = Commandes(annuler_url="{% url 'activites_renseignements' idactivite=activite.idactivite %}", ajouter=False)

        # Affichage
        self.helper.layout = Layout(
            commandes,
            Fieldset("Pièces à fournir",
                Field("pieces"),
            ),
            Fieldset("Cotisations à jour",
                Field("cotisations"),
            ),
            Fieldset("Consentements internet nécessaires",
                Field("types_consentements"),
            ),
            Fieldset("Vaccinations",
                Field("vaccins_obligatoires"),
            ),
        )
