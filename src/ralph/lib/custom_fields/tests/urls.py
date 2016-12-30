from django.conf.urls import include, url

from . import admin, api

cf_tests_urls, cf_tests_app_name, cf_tests_namespace = admin.site.urls

urlpatterns = [
    url(r'^cf_tests_admin/', include((cf_tests_urls, 'ralph', cf_tests_namespace))),
    url(r'^cf_test_api/', include(api.urlpatterns))
]
