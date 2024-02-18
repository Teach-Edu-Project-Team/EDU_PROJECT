from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SignUpTest(TestCase):
    def test_sign_up_page_exists(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_sign_up_user(self):
        user_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        response = self.client.post(reverse('signup'), user_data, format= 'text/html')
        self.assertEqual(response.status_code, 302)
        
        
class BaseSetUp(TestCase):
    
    def SetUp(self):
        user_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        
        self.client.post(reverse('signup'), user_data, format= 'text/html')
        
class ProfileEditTest(TestCase):
    def test_profile_edit(self):
        response = self.client.get(reverse('user_page'))
        self.assertEqual(response.status_code, 200)
        