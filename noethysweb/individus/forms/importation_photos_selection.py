# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import Field
from django_select2.forms import HeavySelect2Widget
from core.forms.base import FormulaireBase


class Formulaire(FormulaireBase, forms.Form):
    individu = forms.ChoiceField(label="Recherchez un individu dans la liste", widget=HeavySelect2Widget({"lang": "fr", "data-width": "100%", "data-ajax--type": "GET"}, data_url="importation_photos_get_individus"), required=False)

    def __init__(self, *args, **kwargs):
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_selection_individu'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('individu'),
        )
