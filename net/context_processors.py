from .models import User

def user_stats(request):
    if request.user.is_authenticated:
        instance = User.objects.get(username=request.user)
        user_followers = instance.follower.all()
        user_followings = instance.followings.all()
        posts = len(instance.posts.all())

        return {'user_posts': posts, 'user_followers': len(user_followers), 'user_followings': len(user_followings)}
    return {}

def context_suggested(request):
    if request.user.is_authenticated:
        exclude_user = User.objects.exclude(username=request.user)[:5]
        store_non_followings = []

        for user in exclude_user:
            if user not in request.user.followings.all():
                store_non_followings.append(user)
                
        return {'context_suggestions': store_non_followings}
    return {}
