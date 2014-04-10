from django.views.decorators.csrf import csrf_exempt
from core.ddb_driver import (
    get_contributor_by_username,
    delete_contributor_by_username,    
    get_contributors,    
    add_album_with_contributor,
    add_contributor,
    )
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseServerError


def get(request, username):

    if username is not None:
        contrib = get_contributor_by_username(username)
        response = HttpResponse(
                content=contrib.json,
                content_type="application/json",
            )
    else:
        contribs = [x.json for x in get_contributors()]
        response = render_to_response(
                "data/list.json",
                {"data": contribs},
                content_type="application/json",
            )
    response['Cache-Control'] = 'no-cache'
    return response

def delete(request, username):
    delete_contributor_by_username(username)
    response = HttpResponse(status=204)
    response['Cache-Control'] = 'no-cache'
    return response


def post(request, username):
    
    #Hacer que el contributor prinmero sea el de sesion
    contrib = add_contributor(username)
    
    response = redirect(reverse("resource_contributor", args=[contrib.username, ]))
    response['Cache-Control'] = 'no-cache'
    return response
         
@csrf_exempt
#@access_required
def entrance(request, *args, **kwargs):
    try:
        if request.method == "GET":
            username = None
            if "username" in kwargs and kwargs["username"] is not None: username = kwargs["username"]
            print( "Buscamos %s" % username) 
            return get(request, username)
    
        if request.method == "DELETE":
            try:
                slug = kwargs["username"]
                return delete(request, username)
            except KeyError:
                return HttpResponseBadRequest(simplejson.dumps({"errors": ["Contributor username missing"]}))
    
        if request.method == "POST":
            print("POST usetrname: %s" % request.POST.get("username"))
            username = request.POST.get("username")
            return post(request, username)
        
    except Exception, er:
        import traceback, sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        response = HttpResponseServerError(
            content=simplejson.dumps({"errors": [str(er), ], "stack": traceback.format_exception(exc_type, exc_value,exc_traceback)}),
            content_type="application/json",
            )
        
        response['Cache-Control'] = 'no-cache'
        return response