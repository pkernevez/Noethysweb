# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from core.views.menu import GetMenuPrincipal
from fiche_famille.utils.utils_famille import LISTE_ONGLETS as LISTE_ONGLETS_FAMILLES
from fiche_individu.utils.utils_individu import LISTE_ONGLETS as LISTE_ONGLETS_INDIVIDUS


def GetPermissionsPossibles(organisateur=None):
    """ Liste des commandes pour créer les permissions des utilisateurs """
    liste_permissions = []

    # Commandes de menu
    menu_principal = GetMenuPrincipal(organisateur=organisateur)
    for menu in menu_principal.GetChildren():
        for sous_menu in menu.GetChildren():
            for commande in sous_menu.GetChildren():
                liste_permissions.append((commande.code, "%s | %s" % (commande.parent.parent.titre, commande.titre)))

    # Fiche famille
    for commande in LISTE_ONGLETS_FAMILLES[1:]:
        liste_permissions.append(("famille_%s" % commande["code"], "Fiche famille | %s" % commande["label"]))

    # Fiche individu
    for commande in LISTE_ONGLETS_INDIVIDUS[1:]:
        liste_permissions.append(("individu_%s" % commande["code"], "Fiche individuelle | %s" % commande["label"]))

    return liste_permissions

