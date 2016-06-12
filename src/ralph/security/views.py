# -*- coding: utf-8 -*-
from ralph.admin.views.extra import RalphDetailView
from ralph.security.models import SecurityScan


class BaseObjectSecurityInfo(
    RalphDetailView
):

    icon = 'lock'
    label = 'Security Info'
    name = 'security_info'
    url_name = 'security_info'
    template_name = 'security/security_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['security_scan'] = SecurityScan.objects.filter(
            base_object=self.object
        ).last()
        return context
