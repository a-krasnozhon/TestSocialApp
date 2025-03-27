import heapq

from models import DB, Post
from response import Response


def create_post(request):
    request.user.create_post(Post(request.content, request.user.username))

    return Response(content=None)


def read_user(request):
    if request.user.username in DB['POST']:
        return Response(content=[str(post) for post in DB['POST'][request.user.username]], multiple=True)
    return Response(content=None)


def follow(request):
    followed = DB['USER'].get(request.content, None)
    if followed:
        request.user.follow(followed)

    return Response(content=None)


def wall(request):
    authors = [request.user.username]
    authors += [username for username in DB['USER'][request.user.username].follows]

    posts = [DB['POST'][author] for author in authors]

    merged_posts = heapq.merge(*posts, key=lambda p: p.created_at.timestamp(), reverse=True)

    return Response(content=[str(post) for post in merged_posts], multiple=True)


AVAILABLE_COMMANDS = {
    '->': create_post,
    '': read_user,
    'follows': follow,
    'wall': wall,
}
