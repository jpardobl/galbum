from django.views.decorators.csrf import csrf_exempt
from core.ddb_driver import (

    get_album_contributors,
    get_album_by_slug,
    delete_album_contributor,
    add_contributor_album,
    )
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson
from django.http import HttpResponseBadRequest, HttpResponse


def get(request, slug):
    """
    Retrieves all the contributors of album by slug
    Does not retrieve by slug and username 
    """
    calbums = [x.json for x in get_album_contributors(get_album_by_slug(slug))]
        
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
            username = kwargs["username"]
            return delete(request, slug, username)
        except KeyError:
            return HttpResponseBadRequest(simplejson.dumps({"errors": ["Album slug missing"]}))

    if request.method == "POST":
        slug = kwargs["slug"]
        username = request.POST["username"]
        return post(request, slug, username)