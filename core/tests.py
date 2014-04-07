from django.test import TestCase

from core.ddb_driver import *
from core.ddb_schema import *


class DynamoDBTest(TestCase):
    
    def test_contributor(self):
        
        contrib = add_contributor("javier")
        
        self.assertEqual(contrib.username, Contributor.get("javier").username,
            "Does not properly create Contributors" 
            )
        
        contrib.delete()
        self.assertEqual(None, Contributor.get("javier"),
            "Does not properly delete contributor")
        
        
        
