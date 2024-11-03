from datetime import datetime
from django.utils.timezone import now

class CheckSubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and has a user_profile
        if request.user.is_authenticated:
            user_profile = request.user
            # Check if subscription has expired
            if user_profile.subscription_end_date and user_profile.subscription_end_date <= now():
                user_profile.subscription_active = False
                user_profile.save()
            else:   
                user_profile.subscription_active = True
                user_profile.save() 

        response = self.get_response(request)
        return response