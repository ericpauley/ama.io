from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class SessionAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return [obj for obj in object_list if obj.user == bundle.request.user]

    def create_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        return [obj for obj in object_list if obj.user == bundle.request.user]

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        return [obj for obj in object_list if obj.user == bundle.request.user]

    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user