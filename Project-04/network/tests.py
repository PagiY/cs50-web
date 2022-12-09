from django.test import TestCase
from .models import Post, User 

# Create your tests here.
class PostTest(TestCase):
    def setUp(self) -> None:
        #create users 
        user1  = User.objects.create(username = 'pagiy')
        
        #create posts
        post1 = Post.objects.create(user = user1, text = 'Post')
        post2 = Post.objects.create(user = user1, text = "Helloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        
    def test_user_post_length(self):
        '''
            check if user post is more 128 characters
        '''
        post = Post.objects.get(id = 2)
        max_length = post._meta.get_field('text').max_length
        self.assertEqual(max_length, 128)
        