from allaccess.views import OAuthCallback
from allaccess.models import Provider, AccountAccess
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

class CustomCallback(OAuthCallback):

    def handle_new_user(self, provider, access, info):
        print(info)
        "Create a shell auth.User and redirect."
        user = self.get_or_create_user(provider, access, info)
        access.user = user
        AccountAccess.objects.filter(pk=access.pk).update(user=user)
        
        if provider.name=="facebook":
            user.first_name = info['first_name']
            user.last_name = info['last_name']
        elif provider.name=="twitter":
            name_parts = info["name"].split()
            if len(name_parts) >= 1:
                user.first_name = name_parts[0]
            if len(name_parts) >= 2:
                user.last_name = name_parts[1]
            user.save()
            if info["verified"]:
                user.meta.verified = True
                user.meta.save()
            access.identifier = info['screen_name']
            access.save()
        user.save()
        user = authenticate(provider=access.provider, identifier=access.identifier)
        login(self.request, user)
        return redirect(self.get_login_redirect(provider, user, access, True))
