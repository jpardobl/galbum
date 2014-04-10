from django.views.decorators.csrf import csrf_exempt
from core.ddb_driver import (
    delete_album_contributor,
    add_contributor_album,
    get_mobjects_by_slug,
    )
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson
from django.http import HttpResponseBadRequest, HttpResponse


def get(request, slug):
    """
    Retrieves all the mobjects of album by slug
    Does not retrieve by slug and mobjectid 
    """
    calbums = [x.tojson for x in get_mobjects_by_slug(slug)]
        
    response = render_to_response(
            "data/list.json",
            {"data": calbums},
            content_type="application/json",
        )
    response['Cache-Control'] = 'no-cache'
    return response

def delete(request, slug, username):
    """
    Deletes a contributor from an album, but the the contributor itself
    """
    delete_album_contributor(slug, username)
    response = HttpResponse(status=204)
    response['Cache-Control'] = 'no-cache'
    return response

def post(request, slug, username):
    """
    Add a contributor to an album, both must previously exist
    """
    add_contributor_album(slug, username)
    response = redirect(reverse("resource_contributoralbum", args=[slug, username]))
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