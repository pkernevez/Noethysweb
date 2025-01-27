# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from django.forms import ModelForm, HiddenInput
from core.forms.base import FormulaireBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden, Submit, HTML, ButtonHolder, Div, Button
from crispy_forms.bootstrap import Field, StrictButton
from core.utils.utils_commandes import Commandes
from core.models import ModeleEmail, Mail, AdresseMail, Rattachement
from django_summernote.widgets import SummernoteInplaceWidget
from outils.widgets import Documents_joints
from django_select2.forms import Select2TagWidget
from outils.forms.editeur_emails import EXTRA_HTML
from core.utils.utils_commandes import Commandes

# class MyWidget(ModelSelect2TagWidget):
#     def label_from_instance(*args):
#         instance = args[1]
#         return instance.individu.Get_nom()


class Formulaire(FormulaireBase, ModelForm):
    objet = forms.CharField(label="Objet", required=False)
    html = forms.CharField(label="Texte", widget=SummernoteInplaceWidget(attrs={'summernote': {'width': '100%', 'height': '200px'}}), required=False)
    documents = forms.CharField(label="Documents", required=False, widget=Documents_joints())
    # dest = forms.ModelMultipleChoiceField(label="Destinataires", required=False, widget=MyWidget(model=Rattachement, search_fields=['individu__nom__icontains', 'individu__prenom__icontains'], attrs={"lang": "fr", "data-width": "100%", "data-minimum-input-length": 0}), queryset=Rattachement.objects.none().order_by("individu__nom", "individu__prenom"))
    dest = forms.MultipleChoiceField(label="Destinataires", required=False, widget=Select2TagWidget(attrs={"lang": "fr", "data-width": "100%", "data-minimum-input-length": 0, "title": "Sélectionnez une adresse dans la liste ou tapez-la directement"}), choices=[])

    class Meta:
        model = Mail
        fields = ["objet", "html", "adresse_exp"]

    def __init__(self, *args, **kwargs):
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form_editeur_emails'
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        # Sélectionne l'adresse d'expédition
        self.fields["adresse_exp"].queryset = AdresseMail.objects.filter(pk__in=self.request.user.Get_adresses_exp_possibles()).order_by("adresse")
        if not self.instance:
            self.fields['adresse_exp'].initial = self.request.user.Get_adresse_exp_defaut()

        # Sélection des destinataires
        if self.instance:
            destinataire = self.instance.destinataires.first()
            liste_dest = []
            selection_defaut = None
            for rattachement in Rattachement.objects.select_related("individu").filter(famille=destinataire.famille):
                for mail in (rattachement.individu.mail, rattachement.individu.travail_mail):
                    if mail:
                        dest = "%s <%s>" % (rattachement.individu.Get_nom(), mail)
                        if mail == destinataire.adresse:
                            selection_defaut = dest
                        liste_dest.append(dest)
            self.fields['dest'].choices = [(dest, dest) for dest in liste_dest]
            if selection_defaut:
                self.fields['dest'].initial = selection_defaut

            if destinataire.documents.all():
                self.fields['documents'].widget.attrs['documents'] = destinataire.documents
            else:
                self.fields['documents'].widget = HiddenInput()

        # Affichage
        self.helper.layout = Layout(
            Hidden("idmail", value=self.instance.pk),
            Commandes(enregistrer=False, ajouter=False, annuler=False,
                      autres_commandes=[
                          HTML("""<a class="btn btn-primary" id="bouton_envoyer" title="Envoyer"><i class="fa fa-send-o margin-r-5"></i>Envoyer</a> """),
                          HTML("""<a class="btn btn-danger" title="Annuler" onclick="$('#modal_editeur_emails').modal('hide');"><i class="fa fa-ban margin-r-5"></i>Annuler</a> """),
                          HTML("""<button type="submit" name="enregistrer_brouillon" title="Enregistrer le brouillon" class="btn btn-default"><i class="fa fa-save margin-r-5"></i>Enregistrer le brouillon</button> """),
                          HTML(EXTRA_HTML),
                      ],
            ),
            Field('objet'),
            Field('adresse_exp'),
            Field('dest'),
            Field('documents'),
            Field('html'),
        )
