from django.views.decorators.csrf import csrf_exempt
from core.ddb_driver import (
    get_album_by_title, 
    get_albums_by_username,
    delete_album_by_slug,
    get_contributor,
    add_album_with_contributor,
    get_album_contributors,
    get_album_by_slug
    )
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson
from django.http import HttpResponseBadRequest


def get(request, slug):
    calbums = get_album_contributors(get_album_by_slug(slug))
        
    response = render_to_response(
            "device/list.json",
            {"data": calbums},
            content_type="application/json",
        )
    response['Cache-Control'] = 'no-cache'
    return response

def delete(request, slug):
    delete_album_by_slug(slug)

def post(request, title):
    contrib = get_contributor(request.user.username)
    album = add_album_with_contributor(title, contrib)
    response = redirect(reverse("resource_album", args=[album.slug, ]))
    response['Cache-Control'] = 'no-cache'
    return response
         
@csrf_exempt
#@access_required
def entrance(request, *args, **kwargs):

    if request.method == "GET":
        slug = kwargs["slug"]
        return get(request, slug)

    if request.method == "DELETE":
        try:
            slug = kwargs["slug"]
            return delete(request, slug)
        except KeyError:
            return HttpResponseBadRequest(simplejson.dumps({"errors": ["Album slug missing"]}))

    if request.method == "POST":
        return post(request)