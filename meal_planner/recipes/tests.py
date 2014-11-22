from django.test import TestCase

from users.models import User
from recipes.models import Recipe

# Create your tests here.
class RecipeTestCase(TestCase):
    def setUp(self):
        self.password1 = 'testpass1'
        self.password2 = 'testpass2'

        self.user1 = User.objects.create_user(
                'test1',
                'test1@test.com',
                self.password1)
        self.user2 = User.objects.create_user(
                'test2',
                'test2@test.com',
                self.password2)

        self.recipe1 = Recipe.objects.create(
                name='apple',
                user=self.user1,
                rating=Recipe.NOT_RATED,
                url='',
                description='')
        self.recipe1.tags.add('tag1', 'tag2')

        self.recipe2 = Recipe.objects.create(
                name='cake',
                user=self.user1,
                rating=Recipe.AWFUL,
                url='http://www.google.com/',
                description='')
        self.recipe2.tags.add('tag2', 'tag3')

        self.recipe3 = Recipe.objects.create(
                name='banana',
                user=self.user1,
                rating=Recipe.GOOD,
                url='',
                description='a test recipe')
        self.recipe3.tags.add('tag1', 'tag3')

        self.recipe4 = Recipe.objects.create(
                name='pie',
                user=self.user2,
                rating=Recipe.BAD,
                url='http://www.test.com/',
                description='')
        self.recipe4.tags.add('test', 'bad')

        self.recipe5 = Recipe.objects.create(
                name='chocolate',
                user=self.user2,
                rating=Recipe.AVERAGE,
                url='',
                description='an average recipe')
        self.recipe5.tags.add('avg')

        self.recipe6 = Recipe.objects.create(
                name='rice',
                user=self.user2,
                rating=Recipe.NOT_RATED,
                url='',
                description='')

        self.recipe7 = Recipe.objects.create(
                name='pasta',
                user=self.user2,
                rating=Recipe.GREAT,
                url='',
                description='great recipe!')
        self.recipe7.tags.add('dinner', 'great')

        self.recipe8 = Recipe.objects.create(
                name='ice cream',
                user=self.user2,
                rating=Recipe.NOT_RATED,
                url='',
                description='need to try')
        self.recipe8.tags.add('todo')

    def test_login_required(self):
        response = self.client.get( '/recipes/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/', 302))

        response = self.client.get(
                '/recipes/view/' + self.recipe1.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/view/' +
                self.recipe1.slug + '/', 302))

        response = self.client.get('/recipes/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/add/', 302))

        response = self.client.post('/recipes/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/add/', 302))

        response = self.client.get(
                '/recipes/edit/' + self.recipe2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/edit/' +
                    self.recipe2.slug + '/', 302))

        response = self.client.post(
                '/recipes/edit/' + self.recipe2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/edit/' +
                    self.recipe2.slug + '/', 302))

        response = self.client.get(
                '/recipes/delete/' + self.recipe2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/delete/' +
                    self.recipe2.slug + '/', 302))

        response = self.client.post(
                '/recipes/delete/' + self.recipe2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/recipes/delete/' +
                    self.recipe2.slug + '/', 302))

    def test_index_auth(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 3)
        self.assertEqual(response.context['recipes'][0]['name'], 'apple')
        self.assertEqual(response.context['recipes'][1]['name'], 'banana')
        self.assertEqual(response.context['recipes'][2]['name'], 'cake')

    def test_index_auth(self):
        self.assertEqual(
                self.client.login(
                    username=self.user1.username,
                    password=self.password1),
                True)
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 3)
        self.assertEqual(response.context['recipes'][0].name, 'apple')
        self.assertEqual(response.context['recipes'][1].name, 'banana')
        self.assertEqual(response.context['recipes'][2].name, 'cake')
        self.client.logout()

    def test_view(self):
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get('/recipes/view/' + self.recipe4.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe'].name, self.recipe4.name)
        self.assertEqual(set(response.context['recipe'].tags.names()),
                set(self.recipe4.tags.names()))
        self.client.logout()

    def test_update(self):
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get('/recipes/edit/' + self.recipe4.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].name, self.recipe4.name)
        self.assertEqual(set(response.context['object'].tags.names()),
                set(self.recipe4.tags.names()))
        response = self.client.post('/recipes/edit/' + self.recipe4.slug + '/',
                { 'rating': Recipe.AVERAGE, 'url': '', 'description': 'new',
                    'tags': 'newtag1, newtag2' }, follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/recipes/', 302))
        updated_recipe = Recipe.objects.get(slug=self.recipe4.slug)
        self.assertEqual(updated_recipe.rating, Recipe.AVERAGE)
        self.assertEqual(updated_recipe.url, '')
        self.assertEqual(updated_recipe.description, 'new')
        self.assertEqual(set(updated_recipe.tags.names()),
                set(['newtag1', 'newtag2']))
        self.client.logout()

    def test_create(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/recipes/add/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/recipes/add/',
                { 'name': 'another test recipe', 'rating': Recipe.GREAT,
                    'url': 'http://www.wonkabar.com/', 'description': 'foobar',
                    'tags': 'scrumdiddlyumptious' }, follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/recipes/', 302))
        created_recipe = Recipe.objects.get(slug='another-test-recipe')
        self.assertEqual(created_recipe.rating, Recipe.GREAT)
        self.assertEqual(created_recipe.url, 'http://www.wonkabar.com/')
        self.assertEqual(created_recipe.description, 'foobar')
        self.assertEqual(set(created_recipe.tags.names()),
                set(['scrumdiddlyumptious']))
        self.client.logout()

    def test_delete(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/recipes/delete/' + self.recipe1.slug + '/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/recipes/delete/' + self.recipe1.slug + '/',
                    follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/recipes/', 302))
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(slug=self.recipe1.slug)
        self.client.logout()
