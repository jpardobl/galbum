from core.ddb_schema import Album, ContributorAlbum, Contributor, Mobject
from boto.dynamodb import condition
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError
#covered
def get_contributor_by_username(username):
    return Contributor.get(username)

#covered
def get_contributors():
    return Contributor.scan({})


#covered
def add_album_with_contributor(title, username):
    """
    Used when creating the album, as it needs to be related to the creator
    """
    album = Album(title=title)    
    album.save()
    ContributorAlbum(slug=album.slug, username=username).save()
    return album    

#covered
def add_contributor_album(slug, username):
    """
    Used when adding an existent contributor to an existent album
    """
    contrib = Contributor.get(username)
    album = Album.get(slug)
    ContributorAlbum(slug=album.slug, username=contrib.username).save()
#covered
def add_contributor(username):
    """
    Used when adding an existent contributor to an existent album
    """
    try:
        get_contributor_by_username(username)
        raise AttributeError("%s username alredy exists" % username)
    except DynamoDBKeyNotFoundError:
        pass
    
   # print( "Username: %s" % username)
    contrib = Contributor(username=username)
    contrib.save()
    return contrib

#covered
def delete_contributor_by_username(username):
    Contributor.get(username).delete()
    [x.delete() for x in ContributorAlbum.scan({"username": condition.EQ(username)})]
        
#covered
def delete_album_by_slug(slug):
    """
    Album deletion can only be done based on slug, thus no conflicts
    """    
    album = get_album_by_slug(slug)
    [x.delete() for x in ContributorAlbum.scan({"slug": condition.EQ(album.slug)})]
    album.delete()
        

#covered
def get_album_by_title(title):
    gen = Album.scan({"title": condition.EQ(title)})
    for data in gen: return data
     
#covered
def get_album_by_slug(slug):
    return Album.get(slug)
#covered
def delete_album_contributor(username, slug):
    ContributorAlbum.get(username, slug).delete()

#covered
def get_album_contributors(album):
    return [Contributor.get(x.username) for x in ContributorAlbum.scan({"slug": condition.EQ(album.slug)})]


def get_mobjects_by_title(title):
    return Mobject.query(title=title)

def get_albums_by_username(username):
    
    return [Album.get(calbum.slug) for calbum in ContributorAlbum.scan({"username": condition.EQ(username)})]
        
    