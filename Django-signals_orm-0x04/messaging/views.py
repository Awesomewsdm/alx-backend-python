from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def delete_user(request):
    """Delete the currently authenticated user and redirect to home.

    This view deletes request.user which triggers the post_delete signal to
    clean up related messaging data.
    """
    user = request.user
    # Log the user out after deletion might be handled by calling logout, but
    # since the user is deleted we'll simply redirect.
    user.delete()
    return redirect("/")
