from rest_framework.permissions import BasePermission


class CanAddOrUpdateCustomer(BasePermission):
    message = "Seuls les utilisateurs de l'équipe commerciale peuvent créer\
        un nouveau client"

    def has_permission(self, request, view):
        """allow to view list customers,

        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view

        Returns:
            [bool] -- true if permission is ok
        """
        if request.method == 'POST':
            return request.user.groups.filter(name='sale').exists()
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
        return request.user.groups.filter(name='sale').exists()


