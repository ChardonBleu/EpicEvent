from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanManage(BasePermission):
    message = "Seuls les utilisateurs de l'équipe commerciale peuvent créer\
un nouveau client. Un commercial ne peut modifier que ses clients. Seuls les \
membre de l'équipe de gestion peuvent supprimer un client."

    def has_permission(self, request, view):
        """allow to view list customers,

        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view

        Returns:
            [bool] -- true if permission is ok
        """
        can_add = request.user.has_perm(
            'CRM.add_customer') or request.user.has_perm(
                'CRM.add_contract') or request.user.has_perm(
                    'CRM.add_event')

        if request.method == 'POST':
            return can_add
        else:
            return True

    def has_object_permission(self, request, view, obj):
        """allow to retrieve, update or delete customer.

        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view
            obj -- current model object

        Returns:
            [bool] -- true if permission is ok
        """

        if view.basename == 'event':
            is_in_charge = obj.support_customuser == request.user
        else:
            is_in_charge = obj.sales_customuser == request.user

        can_delete = request.user.has_perm(
            'CRM.delete_customer') or request.user.has_perm(
                'CRM.delete_contract') or request.user.has_perm(
                    'CRM.delete_event')

        can_view = request.user.has_perm(
            'CRM.view_customer') or request.user.has_perm(
                'CRM.view_contract') or request.user.has_perm(
                    'CRM.view_event')

        can_change = request.user.has_perm(
            'CRM.change_customer') or request.user.has_perm(
                'CRM.change_contract') or request.user.has_perm(
                    'CRM.change_event')

        if request.method == 'DELETE':
            return can_delete
        if request.method in SAFE_METHODS:
            return can_view
        if request.method == 'PUT' or request.method == 'PATCH':
            return can_change or is_in_charge
