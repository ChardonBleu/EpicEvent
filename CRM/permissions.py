from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanManageCustomer(BasePermission):
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
        if request.method == 'POST':
            return request.user.has_perm('CRM.add_customer')
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
        is_in_charge = obj.sales_customuser == request.user
        
        if request.method == 'DELETE':
            return request.user.has_perm('CRM.delete_customer')        
        if request.method in SAFE_METHODS:            
            return request.user.has_perm('CRM.view_customer')
        if request.method == 'PUT' or request.method == 'PATCH':
            return  request.user.has_perm(
                'CRM.change_customer') and is_in_charge


class CanManageContract(BasePermission):
    message = "Seuls les utilisateurs de l'équipe commerciale peuvent créer \
un nouveau contrat pour un client qu'ils gèrent. Un commercial ne \
peut modifier que les contrats qu'il gère. Seuls les \
membre de l'équipe de gestion peuvent supprimer un contrat."

    def has_permission(self, request, view):
        """allow to view list customers,

        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view

        Returns:
            [bool] -- true if permission is ok
        """
        if request.method == 'POST':
            return request.user.has_perm('CRM.add_contract')
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
        is_in_charge = obj.sales_customuser == request.user
       
        if request.method == 'DELETE':
            return request.user.has_perm('CRM.delete_contract')        
        if request.method in SAFE_METHODS:            
            return request.user.has_perm('CRM.view_contract')
        if request.method == 'PUT' or request.method == 'PATCH':
            return  request.user.has_perm(
                'CRM.change_contract') and is_in_charge


class CanManageEvent(BasePermission):
    message = "Seuls les utilisateurs de l'équipe commerciale peuvent créer \
un nouvel évènement pour un client qu'ils gèrent. Seuls les utilisateurs de \
l'équipe de support peuvent modifier les évènements pour un client qu'ils \
gèrent. seuls les membres de l'équipe de gestion peuvent supprimer un \
évènement."

    def has_permission(self, request, view):
        """allow to view list customers,

        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view

        Returns:
            [bool] -- true if permission is ok
        """
        if request.method == 'POST':
            return request.user.has_perm('CRM.add_event')
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
        is_in_charge = obj.support_customuser == request.user
       
        if request.method == 'DELETE':
            return request.user.has_perm('CRM.delete_event')        
        if request.method in SAFE_METHODS:            
            return request.user.has_perm('CRM.view_event')
        if request.method == 'PUT' or request.method == 'PATCH':
            return  request.user.has_perm(
                'CRM.change_event') and is_in_charge
