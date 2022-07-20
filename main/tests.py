from django.test import TestCase
from .models import *
# Create your tests here.
class slattTestCase(TestCase):
    class AnimalTestCase(TestCase):
        def setUp(self):
            print(Customer.objects.get(id=5).fav_films.all())

        def test_animals_can_speak(self):
            """Animals that can speak are correctly identified"""


