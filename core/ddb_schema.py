from dynamodb_mapper.model import DynamoDBModel


class Contributor(DynamoDBModel):
    __table__ = u"contributor"
    __hash_key__ = u"username"
    __schema__ = {
        u"username": unicode,
      }
 
class Album(DynamoDBModel):
    __table__ = u"album"
    __hash_key__ = u"title"
    __schema__ = {
        u"title": unicode,
        u"slug": autoincrement_int,
      }
    
class ContributorAlbum(DynamoDBModel):
    __table__ = u"contributor_album"
    __hash_key__ = u"username"
    __range_key__ = u"title"
    __schema__ = {
        u"username": unicode,
        u"title": unicode,        
      }
    
class Mobject(DynamoDBModel):
    __table__ = u"mobject"
    __hash_key__ = u"title"
    __range_key__ = u"mobjectid"
    __schema__ = {
        u"title": unicode,
        u"mobjectid": autoincrement_int,
        u"url": unicode,
    }