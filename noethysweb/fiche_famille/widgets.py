# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
from core.models import Facture, Consommation
from core.utils import utils_dates


class Selection_emetteur(Widget):
    template_name = 'fiche_famille/widgets/emetteur.html'

    # class Media:
    #     css = {"all": ("//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/css/select2.min.css",)}
    #     js = ("django_select2/django_select2.js", "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/select2.min.js",
    #           "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/i18n/fr.js")

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        context['choices'] = self.choices
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class Selection_mode_reglement(Widget):
    template_name = 'fiche_famille/widgets/mode_reglement.html'

    # class Media:
    #     css = {"all": ("//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/css/select2.min.css",)}
    #     js = ("django_select2/django_select2.js", "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/select2.min.js",
    #           "//cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/i18n/fr.js")

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        context['choices'] = self.choices
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class Saisie_ventilation(Widget):
    template_name = 'fiche_famille/widgets/ventilation.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))



class Internet_identifiant(Widget):
    template_name = 'fiche_famille/widgets/internet_identifiant.html'

    class Media:
        js = ("lib/bootbox/bootbox.min.js",)

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class Internet_mdp(Widget):
    template_name = 'fiche_famille/widgets/internet_mdp.html'

    class Media:
        js = ("lib/bootbox/bootbox.min.js",)

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class Facture_prestation(Widget):
    template_name = 'fiche_famille/widgets/facture_prestation.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        facture = Facture.objects.get(pk=value) if value else None
        if facture:
            context['texte'] = "Facture n°%d du %s" % (facture.numero, utils_dates.ConvertDateToFR(facture.date_edition))
        else:
            context['texte'] = "Aucune facture associée"
        context['facture'] = facture
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class Consommations_prestation(Widget):
    template_name = 'fiche_famille/widgets/consommations_prestation.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        consommations = Consommation.objects.select_related("unite").filter(prestation_id=value) if value else None
        context['consommations'] = consommations
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))
