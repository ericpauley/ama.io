from tastypie.authorization import Authorization,ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized
from questions.models import AMAAnswer
from django.utils import timezone
import datetime

def permcheck(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            return result
        else:
            raise Unauthorized()
    return inner

class SessionAuthorization(Authorization):
    @permcheck
    def read_list(self, object_list, bundle):
        return object_list

    @permcheck
    def read_detail(self, object_list, bundle):
        return True

    @permcheck
    def create_list(self, object_list, bundle):
        return [obj for obj in object_list if obj.user == bundle.request.user]

    @permcheck
    def create_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    @permcheck
    def update_list(self, object_list, bundle):
        return [obj for obj in object_list if obj.user == bundle.request.user]

    @permcheck
    def update_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    @permcheck
    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        return [obj for obj in object_list if obj.user == bundle.request.user]

    @permcheck
    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

class CommentAuthorization(ReadOnlyAuthorization):
    def create_detail(self, object_list, bundle):
        if bundle.request.user.is_authenticated():
            if bundle.request.user.comments.filter(created__gte=timezone.now() - datetime.timedelta(minutes=1)).count():
                return False
            else:
                return True
        else:
            return False

class QuestionAuthorization(ReadOnlyAuthorization):
    
    @permcheck
    def delete_detail(self, object_list, bundle):
        if bundle.obj.asker != bundle.request.user:
            return False
        try:
            answer = bundle.obj.answer
            return False
        except AMAAnswer.DoesNotExist:
            return True
        return bundle.obj.session.state != 'after'

