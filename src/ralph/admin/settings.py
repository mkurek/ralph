from constance import admin

from ralph.admin.decorators import register

register([admin.Config], admin.ConstanceAdmin)
