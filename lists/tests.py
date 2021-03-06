from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_can_redirect_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(),0)

    def test_displays_all_list_items(self):
        #setup
        Item.objects.create(text="itemy 1")
        Item.objects.create(text="itemy 2")
        #exercise - actually calls the code under test
        response = self.client.get("/")
        #assert
        self.assertEqual("itemy 1", response.content.decode())
        self.assertEqual("itemy 2", response.content.decode())

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "This is the first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "This is the second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "This is the first (ever) list item")
        self.assertEqual(second_saved_item.text, "This is the second item")
