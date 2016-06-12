from libcloud.compute.types import NodeState
from django.utils.translation import ugettext_lazy as _
from pony_admin.admin import BaseAdmin


class ComputeAdmin(BaseAdmin):
    list_display = ['id', 'name', 'get_state']

    def get_objects(self, request):
        nodes = self.model.compute.list_nodes()
        return nodes

    def get_state(self, obj):
        return NodeState.tostring(obj.state)
    get_state.short_description = _("State")
