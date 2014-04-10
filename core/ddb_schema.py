from dynamodb_mapper.model import DynamoDBModel, autoincrement_int
import simplejson
from django.core.urlresolvers import reverse

class Contributor(DynamoDBModel):
    __table__ = u"contributor"
    __hash_key__ = u"username"
    __schema__ = {
        u"username": unicode,
      }
    @property
    def json(self):
        return self.to_json()
    
    def to_json(self):
        return simplejson.dumps({
                "type": "Contributor", 
                "username": self.username,
                "url": reverse("resource_contributor", kwargs={"username": self.username, })})
        
    def save(self, *args, **kwargs):
        #TODO COmprobar si es nuevo
        if is_new:
            if Contributor.get(self.username):
                raise AttributeError("Contributor with username %s already exists at the DB" % self.username)
        super(Contributor, self).save(*args, **kwargs)
        
class Album(DynamoDBModel):
    __table__ = u"album"
    __hash_key__ = u"slug"
    __schema__ = {
        u"title": unicode,
        u"slug": autoincrement_int,        
      }
    @property
    def json(self):
        return self.to_json()
    
    def to_json(self):
        return simplejson.dumps({
            "type": "Album", 
            "slug": self.slug, 
            "title": self.title, 
            "url": reverse("resource_album", kwargs={"slug": self.slug, })})
    
class ContributorAlbum(DynamoDBModel):
    __table__ = u"contributor_album"
    __hash_key__ = u"username"
    __range_key__ = u"slug"
    __schema__ = {
        u"username": unicode,
        u"slug": int,        
      }
    @property
    def json(self):
        return self.to_json()
    
    def to_json(self):
        return simplejson.dumps({
            "type": "ContributorAlbum", 
            "slug": self.slug, 
            "username": self.username,
            "url": reverse("resource_contributoralbum", 
                           kwargs={"slug": self.slug, "username": self.username})})
        
           
    def save(self, *args, **kwargs):
        #TODO COmprobar si es nuevo
        if is_new:
            if ContributorAlbum.get(self.username, self.slug):
                raise AttributeError(
                    "Contributor with username %s already associated and album with title: %s" % 
                    (self.username, self.slug))
        
        super(ContributorAlbum, self).save(*args, **kwargs)
        
class ViewerAlbum(DynamoDBModel):
    __table__ = u"viewer_album"
    __hash_key__ = u"username"
    __range_key__= u"slug"
    __schema__ = {
        u"username": unicode,
        u"slug": int,         
        }
    @property
    def json(self):
        return self.to_json()
    
    def to_json(self):
        return simplejson.dumps({
            "type": "ViewerAlbum", 
            "slug": self.slug, 
            "username": self.username,
            "url": reverse("resource_vieweralbum", 
                           kwargs={"slug": self.slug, "username": self.username})})
    def save(self, *args, **kwargs):
        #TODO COmprobar si es nuevo
        if is_new:
            if ViewerAlbum.get(self.username, self.slug):
                raise AttributeError(
                    "Contributor with username %s already associated and album with title: %s" % 
                    (self.username, self.slug))
        super(ViewerAlbum, self).save(*args, **kwargs)
                
class Mobject(DynamoDBModel):
    __table__ = u"mobject"
    __hash_key__ = u"slug"
    __range_key__ = u"mobjectid"
    __schema__ = {
        u"slug": int,
        u"mobjectid": autoincrement_int,
        
    }
    @property
    def json(self):
        return self.to_json()
    
    def to_json(self):
        return simplejson.dumps({
            "type": "Mobject", 
            "slug": self.slug, 
            "mobjectid": self.mobjectid,
            "url": reverse("resource_mobject", 
                    kwargs={"slug": self.slug, "mobjectid": self.mobjectid})
            })
        
class Sessions(DynamoDBModel):
   __table__ = u"Sessions"
   __hash_key__ = u"session_key"
   __schema__ = {
      u"session_key": unicode,
   }