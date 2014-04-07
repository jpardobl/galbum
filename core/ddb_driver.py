from core.ddb_schema import Album, ContributorAlbum, Contributor, Mobject


def get_contributor_by_username(username):
    return Contributor.get(username)

def get_contributors():
    return Contributor.query()


def add_album_with_contributor(title, contributor):
    """
    Used when creating the album, as it needs to be related to the creator
    """
    album = Album()
    album.title = title
    album.save()
    ContributorAlbum(title=title, username=contributor.username).save()
    return album    

def add_contributor_album(slug, username):
    """
    Used when adding an existent contributor to an existent album
    """
    contrib = Contributor.get(username)
    album = Album.get(slug)
    ContributorAlbum(slug=album.slugm, username=contrib.username).save()

def add_contributor(username):
    """
    Used when adding an existent contributor to an existent album
    """
    print( "Username: %s" % username)
    contrib = Contributor(username=username)
    contrib.save()
    return contrib
    
        
def delete_album_by_slug(slug):
    get_album_by_slug(slug).delete()

def delete_contributor_by_username(username):
    Contributor.get(username).delete()
    
def get_album_by_title(title):
    return Album.query(title=title)

def get_album_by_slug(slug):
    return Album.get(slug)

def delete_album_contributor(slug, username):
    ContributorAlbum.query(slug, username).delete()

def get_album_contributors(album):
    return [Contributor.get(x.username) for x in ContributorAlbum.query(title=album.title)]

def get_mobjects_by_slug(slug):
    return Mobject.query(slug=slug)

def get_albums_by_username(username):
    
    return [Album.get(album.title) for album in ContributorAlbum.query(username=username)]
        
    