from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            complete_profile_url = reverse('market:complete_profile')
            logout_url = reverse('account_logout')

            # Ruxsat etilgan yo'llar: profil to'ldirish, chiqish, allauth, admin panel, api, media, static
            allowed_prefixes = [
                complete_profile_url,
                logout_url,
                '/accounts/',
                '/django-secret-admin/',
                '/adminnn/',
                '/dashboard/',
                '/api/',
                '/media/',
                '/static/',
            ]

            is_allowed = any(request.path.startswith(p) for p in allowed_prefixes)

            if not is_allowed:
                user = request.user
                profile = getattr(user, 'profile', None)

                # Profil to'liq hisoblanishi uchun kerakli maydonlar
                is_complete = (
                    user.first_name and
                    profile and
                    profile.phone_number and
                    profile.address
                )

                if not is_complete:
                    return redirect(complete_profile_url)

        response = self.get_response(request)
        return response


import uuid

class GuestUUIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        guest_uuid = request.COOKIES.get('guest_uuid')
        if not guest_uuid:
            guest_uuid = str(uuid.uuid4())
            request.guest_uuid = guest_uuid
        else:
            request.guest_uuid = guest_uuid
            
        response = self.get_response(request)
        
        # Set cookie if it was just generated
        if not request.COOKIES.get('guest_uuid'):
            response.set_cookie('guest_uuid', guest_uuid, max_age=365*24*60*60)  # 1 year
            
        return response
