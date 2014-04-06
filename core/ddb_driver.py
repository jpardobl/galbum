from core.ddb_schema import Album, ContributorAlbum, Contributor


def get_contributor(username):
    return Contributor.get(username=username)


def add_album_with_contributor(title, contributor):
    
    album = Album()
    album.title = title
    album.save()
    ContributorAlbum(title=title, username=contributor.username).save()
    return album    
    
def delete_album_by_slug(slug):
    Album(slug=slug).delete()

def get_album_by_title(title):
    return Album.get(title=title)

def get_album_by_slug(slug):
    return Album.get(slug=slug)

def get_album_contributors(album):
    return [Contributor.get(username=x.username) for x in ContributorAlbum.query(title=album.title)]

def get_albums_by_username(username):
    
    return [Album.get(album.title) for album in ContributorAlbum.query(username=username)]
        
    