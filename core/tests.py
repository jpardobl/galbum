from django.test import TestCase
from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError
from core.ddb_driver import *
from core.ddb_schema import *
#from dynamodb_mapper.model.DynamoDBModel.
import logging

logging.basicConfig(level=logging.INFO)
class DynamoDBTest(TestCase):
    
    def setUp(self):
        logging.info("Setting up the environment")
        print("Vamos a borrar los contributors")
        [x.delete() for x in Contributor.scan()]            
        [x.delete() for x in Album.scan()]
        [x.delete() for x in ContributorAlbum.scan()] 
        [x-delete() for x in Mobject.scan()]
    
    def test_viewer(self):
        logging.info("*************** Testing viewers started *************")
        
        logging.info("Test method: add_viewer_album ....")
        title = "ranciion"
        album = add_album(title)
        username = u"ramala"
        viewer = add_viewer_album(username, album.slug)
        
        viewer_db = ViewerAlbum.get(username, album.slug)
        
        self.assertEquals(
            viewer_db.username,
            viewer.username,
            "Not properly adding a viewer to an album",
            )
        logging.info("Testing viewer duplication avoidance")
        self.assertRaises(
            AttributeError,
            add_viewer_album,
            username,
            album.slug,
            )
        logging.info("Test method: del_viewer_album ....")
        
        delete_viewer_album(username, album.slug)
        
        self.assertRaises(
            DynamoDBKeyNotFoundError,
            ViewerAlbum.get,
            username, album.slug,
            )
        logging.info("Testing viewer deletion, when album deletion")
        add_viewer_album(username, album.slug)
        delete_album_by_slug(album.slug)
        self.assertRaises(
            DynamoDBKeyNotFoundError,
            ViewerAlbum.get,
            username, album.slug,
            )
        
        logging.info("*************** Testing viewers ended ***************")
        
    def test_contributor(self):
        #self.setUp()
        logging.info("Testing contributors started")
        logging.info("Testing method: add_contributor")
        
        contrib = add_contributor(u"javier")
        
        self.assertEqual(contrib.username, Contributor.get(u"javier").username,
            "Does not properly create Contributors" 
            )
        logging.info("Testing contributor duplication avoidance")
        self.assertRaises(
            AttributeError,
            add_contributor,
            u"javier",
            
            )
        
        logging.info("Testing method: get_contributor_by_username")
        
        contrib = get_contributor_by_username(u"javier")
        self.assertEqual(contrib.username, u"javier",
            "Does not properly retrieve with method:get_contributor_by_username")
        
        logging.info("Testing method: del_contributor_by_username")
        delete_contributor_by_username(u"javier")
        
        self.assertRaises(
            DynamoDBKeyNotFoundError,
            Contributor.get,
            u"javier",
            "Does not properly delete contributor"
            )
        
        logging.info("Testing method: get_contributors")
        add_contributor(u"juanjo")
        add_contributor(u"jorge")
        
        contribss = [x.username for x in get_contributors()]
        
        self.assertTrue(u"juanjo" in contribss ,
                "Not properly added juanjo to contributors")
        self.assertTrue(u"jorge" in contribss ,
                "Not properly added jorge to contributors")
        
        
        alb = 
        
        logging.info(" ******* Testing contributors ended ********** ")
    def test_album(self):
        #self.setUp()
        logging.info("***** Testing album started ****** ")
        contrib = Contributor(username=u"javier")
        contrib.save()
        logging.info("Testing method: add_album_with_contributor")
        titulo = u"titulo del album"
        add_album_with_contributor(titulo, contrib.username)
        album = get_album_by_title(titulo)
        self.assertEquals(
                album.title,
                titulo,
                "add_album_with_contributor does not properly create the album"                
            )
        
        logging.info("Testing duplication of album for contributor avoidance")
        self.assertRaises(
            AttributeError,
            add_album_with_contributor,
            titulo,
            contrib.username,
            )
        ca = ContributorAlbum.get(contrib.username, album.slug)
        self.assertEquals(
            album.slug,
            ca.slug,
            "add_album_with_contributor does not properly attach Album to creator"
            )
        
        logging.info("Testing mehod: add_contributor_album")
        contrib1 = add_contributor(u"Roger1")
        add_contributor_album(album.slug, contrib1.username)
        
        contribs = [x.username for x in get_album_contributors(album)]

        self.assertTrue(u"javier" in contribs and u"Roger1" in contribs,
            "add_contributor_album does not properly add an existent contributor to an existent album")
        
        logging.info("Testing: delete_contributor_by_username")
        
        delete_contributor_by_username(u"javier")
        self.assertRaises(
            DynamoDBKeyNotFoundError,
            Contributor.get,
            u"javier",
            "delete_contributor_by_username Does not properly delete contributor"
            )
        
        contribs = [x.username for x in get_album_contributors(album)]
        self.assertTrue(not u"javier" in contribs,
            "delete_contributor_by_username Does not properly delete contributor from an album once the contributor is been deleted")
        
        
        logging.info("Testing method: delete_album_by_slug")
        title = album.title
        delete_album_by_slug(album.slug)
        #print( "el album**************** %s " % get_album_by_title(title))
        self.assertEquals(
            None,
            get_album_by_title(title),
            "delete_album_by_slug no properly deletes the album",
            )
        for x in ContributorAlbum.scan({"title": condition.EQ(album.title)}):
            self.assertTrue(True, "delete_album_by_slug does not properly delete the album contributors")
        
        logging.info("Testing method: get_album_by_slug")
        a1 = Album(title=u"rodolgo es un titulo")
        a1.save()
        aa1 = get_album_by_slug(a1.slug)
        self.assertEquals(a1.title, aa1.title, "get_album_by_slug does not properly retrieve the album")
        
        logging.info("Testing method: delete_album_contributor")
        add_contributor_album(a1.slug, contrib1.username)
        self.assertNotEqual(
                None,                
                ContributorAlbum.query(a1.slug, condition.EQ(contrib1.username)),
                "add_contributor_album not properly adding contributor to album",
            )
   #     print "slug: %s" % a1.slug
   #     print "usernma:E %s" % contrib1.username
        delete_album_contributor(contrib1.username, a1.slug)
        for x in ContributorAlbum.query(contrib1.username, condition.EQ(a1.slug)):
            self.assertTrue(
                True,                
                "delete_album_contributor not properly deleting contributor from album",
            )
        
        
        logging.info("Testing method: get_albums_by_username")
        add_contributor_album(a1.slug, contrib1.username)
        self.assertEquals(1,len(get_albums_by_username(contrib1.username)),
                          "get_albums_by_username not properly retrieving albums by username")
        
        logging.info(" ************** Testing albums ended ************* ")
