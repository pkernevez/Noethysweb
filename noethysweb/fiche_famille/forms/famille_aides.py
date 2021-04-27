# -*- coding: utf-8 -*-

#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden, Submit, HTML, Fieldset, ButtonHolder, Div
from crispy_forms.bootstrap import Field, StrictButton, PrependedText, InlineCheckboxes
from core.utils.utils_commandes import Commandes
from core.models import Famille, Aide, CombiAide, Rattachement, JOURS_SEMAINE, Rattachement, Individu, CombiAide, Unite, Activite
from core.widgets import DatePickerWidget, Formset
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from core.utils import utils_preferences



class CombiAideForm(forms.ModelForm):
    unites = forms.ModelMultipleChoiceField(label="Combinaison conditionnelle d'unités", widget=Select2MultipleWidget({"lang":"fr"}), queryset=Unite.objects.none(), required=False)

    class Meta:
        model = CombiAide
        exclude = []

    def __init__(self, *args, activite, **kwargs):
        super(CombiAideForm, self).__init__(*args, **kwargs)
        self.activite = activite

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['unites'].queryset = Unite.objects.filter(activite=activite)

    def clean(self):
        if self.cleaned_data.get('DELETE') == False:

            # Vérifie qu'au moins une unité a été saisie
            if len(self.cleaned_data["unites"]) == 0:
                raise forms.ValidationError('Vous devez sélectionner au moins une unité')

        return self.cleaned_data


class BaseCombiAideFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.activite = kwargs.get("activite", None)
        super(BaseCombiAideFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        index_ligne = 0
        liste_lignes_unites = []
        for form in self.forms:
            if self._should_delete_form(form) == False:

                # Vérification de la validité de la ligne
                if form.is_valid() == False or len(form.cleaned_data) == 0:
                    message = form.errors.as_data()["__all__"][0].message
                    raise forms.ValidationError("La ligne %d n'est pas valide : %s." % (index_ligne+1, message))

                # Vérifie que 2 lignes ne sont pas identiques sur les unités
                dict_ligne = form.cleaned_data
                if str(dict_ligne["unites"]) in liste_lignes_unites:
                    raise forms.ValidationError("Deux combinaisons d'unités semblent identiques")

                liste_lignes_unites.append(str(dict_ligne["unites"]))
                index_ligne += 1

        # Vérifie qu'au moins une ligne a été saisie
        if index_ligne == 0:
            raise forms.ValidationError("Vous devez saisir au moins une combinaison d'unités")


FORMSET_COMBI = inlineformset_factory(Aide, CombiAide, form=CombiAideForm, fk_name="aide", formset=BaseCombiAideFormSet,
                                            fields=["montant", "unites"], extra=0, min_num=1,
                                            can_delete=True, validate_max=True, can_order=False)



class Formulaire(ModelForm):
    montant_max = forms.DecimalField(label="Montant plafond", max_digits=6, decimal_places=2, initial=0.0, required=False)
    jours_scolaires = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=JOURS_SEMAINE)
    jours_vacances = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=JOURS_SEMAINE)
    individus = forms.ModelMultipleChoiceField(label="Bénéficiaires", widget=Select2MultipleWidget({"lang":"fr"}), queryset=Individu.objects.none(), required=True)

    class Meta:
        model = Aide
        fields = "__all__"
        widgets = {
            'date_debut': DatePickerWidget(),
            'date_fin': DatePickerWidget(),
        }

    def __init__(self, *args, **kwargs):
        idfamille = kwargs.pop("idfamille")
        idactivite = kwargs.pop("idactivite")
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'famille_aides_form'
        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 col-form-label'
        self.helper.field_class = 'col-md-10'

        # Définit la famille associée
        famille = Famille.objects.get(pk=idfamille)

        # Activité
        if self.instance.idaide != None:
            idactivite = self.instance.activite.idactivite

        self.fields["activite"].initial = Activite.objects.get(pk=idactivite).idactivite
        self.fields["activite"].disabled = True

        # Individus bénéficiaires
        individus = [rattachement.individu_id for rattachement in Rattachement.objects.filter(famille=famille)]
        self.fields['individus'].queryset = Individu.objects.filter(pk__in=individus).order_by("nom")

        # Jours
        self.fields["jours_scolaires"].initial = [0, 1, 2, 3, 4]
        self.fields["jours_vacances"].initial = [0, 1, 2, 3, 4]

        # Affichage
        self.helper.layout = Layout(
            Commandes(annuler_url="{{ view.get_success_url }}"),
            Hidden('famille', value=idfamille),
            Fieldset("Généralités",
                Field('activite'),
                Field('nom'),
                Field('caisse'),
                Field('date_debut'),
                Field('date_fin'),
            ),
            Fieldset("Bénéficiaires",
                Field("individus"),
            ),
            Fieldset("Montants",
                Div(
                    Div(
                        HTML("<label class='col-form-label col-md-2 requiredField'><b>Montants*</b></label>"),
                        Div(
                            Formset("formset_combi"),
                            css_class="controls col-md-10"
                        ),
                        css_class="form-group row"
                    ),
                ),
            ),
            Fieldset("Options",
                InlineCheckboxes('jours_scolaires'),
                InlineCheckboxes('jours_vacances'),
                PrependedText('montant_max', utils_preferences.Get_symbole_monnaie()),
                Field('nbre_dates_max'),
            ),
        )

    def clean(self):
        return self.cleaned_data




class Formulaire_selection_activite(forms.Form):
    activite = forms.ModelChoiceField(label="Activité", widget=Select2Widget({"lang":"fr"}), queryset=Activite.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(Formulaire_selection_activite, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('activite'),
            ButtonHolder(
                Submit('submit', _('Valider'), css_class='btn-primary'),
                HTML("""<a class="btn btn-danger" href="{{ view.Get_annuler_url }}"><i class='fa fa-ban margin-r-5'></i>Annuler</a>"""),
                css_class="pull-right",
            )
        )
