from django.contrib import admin
from users.models import Profile , PlatformReview
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','role']
    list_filter = ['role']
    search_fields = ['user__name','user__email']

    def get_form(self, request, obj=None, **kwargs):
        # This method controls which fields are editable
        form = super().get_form(request, obj, **kwargs)
        # If the logged-in user is NOT a superuser, make the 'role' field read-only
        if not request.user.is_superuser:
            form.base_fields['role'].disabled = True
        return form
admin.site.register(PlatformReview)