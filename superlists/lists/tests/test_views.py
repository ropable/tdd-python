from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_LIST_ERROR
from lists.models import Item, List
from lists.views import home_page
from unittest import skip


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(list_.pk))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/{0}/'.format(correct_list.pk))

        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='item 3', list=other_list)
        Item.objects.create(text='item 4', list=other_list)

        response = self.client.get('/lists/{0}/'.format(correct_list.pk))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'item 3')
        self.assertNotContains(response, 'item 4')

    def can_save_a_POST_request_to_an_existing_link(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{0}/'.format(correct_list.pk),
            data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        self.assertNotEqual(new_item.list, other_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{0}/'.format(correct_list.pk),
            data={'text': 'A new item for an existing list'})

        self.assertRedirects(response, '/lists/{0}/'.format(correct_list.pk))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(list_.pk))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/{0}/'.format(list_.pk), data={'text': ''})

    def test_invalid_input_means_nothing_saved_to_db(self):
        self.post_invalid_input()
        listey = List.objects.create()
        self.assertEqual(Item.objects.all().count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_renders_form_with_errors(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, escape(EMPTY_LIST_ERROR))


class HomePageTest(TestCase):
    maxDiff = None

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
        # Use decode() to convert the response.content bytes into a unicode
        # string, so we can compare strings with strings instead of bytes.
        expected_html = render_to_string('home.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(List.objects.all().count(), 1)

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.all()[0]
        self.assertRedirects(response, '/lists/{0}/'.format(new_list.pk))

    def test_validation_errors_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.all().count(), 0)
        self.assertEqual(Item.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        self.assertIsInstance(response.context['form'], ItemForm)
