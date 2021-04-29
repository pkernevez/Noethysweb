#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core.views import erreurs


urlpatterns = [
    path(settings.URL_GESTION, admin.site.urls),
    path(settings.URL_BUREAU, include('core.urls')),
    path(settings.URL_BUREAU, include('parametrage.urls')),
    path(settings.URL_BUREAU, include('outils.urls')),
    path(settings.URL_BUREAU, include('individus.urls')),
    path(settings.URL_BUREAU, include('fiche_famille.urls')),
    path(settings.URL_BUREAU, include('fiche_individu.urls')),
    path(settings.URL_BUREAU, include('cotisations.urls')),
    path(settings.URL_BUREAU, include('consommations.urls')),
    path(settings.URL_BUREAU, include('facturation.urls')),
    path(settings.URL_BUREAU, include('reglements.urls')),
    path(settings.URL_BUREAU, include('aide.urls')),
    path('select2/', include('django_select2.urls')),
    path('summernote/', include('django_summernote.urls')),
]

# Ajout de l'URL du portail
if settings.PORTAIL_ACTIF:
    urlpatterns.append(path(settings.URL_PORTAIL, include('portail.urls')))

if settings.DEBUG:
    # Ajoute le répertoire Media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Ajoute le debugtoolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


# Modifie les noms dans l'admin
admin.site.site_header = "Administration de Noethysweb"
admin.site.index_title = "Noethysweb"
admin.site.site_title = "Administration"

# Personnalisation des pages d'erreur
handler403 = erreurs.erreur_403
handler404 = erreurs.erreur_404
handler500 = erreurs.erreur_500