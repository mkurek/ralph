from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from ralph.admin import RalphTabularInline
from ralph.admin.m2m import RalphTabularM2MInline
from ralph.admin.views.extra import RalphDetailViewAdmin
from ralph.assets.models.components import Ethernet
from ralph.lib.table import TableWithUrl
from ralph.networks.forms import NetworkForm, NetworkInlineFormset
from ralph.networks.models import Network
from ralph.data_center.forms import DataCenterAssetForm


class NetworkInline(RalphTabularInline):
    form = NetworkForm
    formset = NetworkInlineFormset
    model = Ethernet
    exclude = ['model', 'speed', 'label', 'is_management']

    def get_queryset(self, request):
        # TODO: move somewhere else
        messages.warning(
            request, 'Main hostname ({}) not found in one of attached IPs'.format('s51407.dc5.alledc.net')
        )
        return super().get_queryset(request).filter(
            ipaddress__is_management=False
        ).order_by('-mac', '-ipaddress__hostname', 'ipaddress__address')


class NetworkTerminatorReadOnlyInline(RalphTabularM2MInline):
    model = Network
    extra = 0
    show_change_link = True
    verbose_name_plural = _('Terminators of')
    fields = [
        'name', 'address',
    ]

    def get_readonly_fields(self, request, obj=None):
        return self.get_fields(request, obj)

    def has_add_permission(self, request):
        return False


class NetworkView(RalphDetailViewAdmin):
    icon = 'chain'
    name = 'network'
    label = 'Network'
    url_name = 'network'
    admin_attribute_list_to_copy = [
        'available_networks', 'available_environments', 'form'
    ]
    readonly_fields = ('available_networks', 'available_environments')
    inlines = [
        NetworkInline,
    ]
    form = DataCenterAssetForm  # TODO: fix for vm
    fieldsets = (
        (_(''), {
            'fields': (
                'hostname', 'management_ip', 'management_hostname',
                'manage_management_dns'
            )
        }),
        (_(''), {
            'fields': (
                'available_networks',
                'available_environments',
            )
        }),
    )

    def available_networks(self, instance):
        networks = instance._get_available_networks(
            as_query=True
        ).select_related('network_environment')
        if networks:
            result = TableWithUrl(
                networks,
                ['name', 'address', 'network_environment', 'get_first_free_ip'],
                url_field='name',
            ).render()
        else:
            result = '&ndash;'
        return result
    available_networks.short_description = _('Available networks')
    available_networks.allow_tags = True

    def available_environments(self, instance):
        network_envs = instance._get_available_network_environments(
            as_query=True
        )
        if network_envs:
            result = TableWithUrl(
                network_envs,
                [('name', 'Environment'), 'get_next_free_hostname'],
                url_field='name',
            ).render()
        else:
            result = '&ndash;'
        return result
    available_environments.short_description = _(
        'Available network environments'
    )
    available_environments.allow_tags = True


class NetworkWithTerminatorsView(NetworkView):
    inlines = [
        NetworkInline,
        NetworkTerminatorReadOnlyInline,
    ]
