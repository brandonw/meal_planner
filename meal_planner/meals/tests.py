from django.test import TestCase

from users.models import User
from meals.models import Meal

# Create your tests here.
class MealTestCase(TestCase):
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

        self.meal1 = Meal.objects.create(
                name='apple',
                user=self.user1,
                rating=Meal.NOT_RATED,
                url='',
                description='')
        self.meal1.tags.add('tag1', 'tag2')

        self.meal2 = Meal.objects.create(
                name='cake',
                user=self.user1,
                rating=Meal.AWFUL,
                url='http://www.google.com/',
                description='')
        self.meal2.tags.add('tag2', 'tag3')

        self.meal3 = Meal.objects.create(
                name='banana',
                user=self.user1,
                rating=Meal.GOOD,
                url='',
                description='a test meal')
        self.meal3.tags.add('tag1', 'tag3')

        self.meal4 = Meal.objects.create(
                name='pie',
                user=self.user2,
                rating=Meal.BAD,
                url='http://www.test.com/',
                description='')
        self.meal4.tags.add('test', 'bad')

        self.meal5 = Meal.objects.create(
                name='chocolate',
                user=self.user2,
                rating=Meal.AVERAGE,
                url='',
                description='an average meal')
        self.meal5.tags.add('avg')

        self.meal6 = Meal.objects.create(
                name='rice',
                user=self.user2,
                rating=Meal.NOT_RATED,
                url='',
                description='')

        self.meal7 = Meal.objects.create(
                name='pasta',
                user=self.user2,
                rating=Meal.GREAT,
                url='',
                description='great meal!')
        self.meal7.tags.add('dinner', 'great')

        self.meal8 = Meal.objects.create(
                name='ice cream',
                user=self.user2,
                rating=Meal.NOT_RATED,
                url='',
                description='need to try')
        self.meal8.tags.add('todo')

    def test_login_required(self):
        response = self.client.get( '/meals/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/', 302))

        response = self.client.get(
                '/meals/view/' + self.meal1.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/view/' +
                self.meal1.slug + '/', 302))

        response = self.client.get('/meals/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/add/', 302))

        response = self.client.post('/meals/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/add/', 302))

        response = self.client.get(
                '/meals/edit/' + self.meal2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/edit/' +
                    self.meal2.slug + '/', 302))

        response = self.client.post(
                '/meals/edit/' + self.meal2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/edit/' +
                    self.meal2.slug + '/', 302))

        response = self.client.get(
                '/meals/delete/' + self.meal2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/delete/' +
                    self.meal2.slug + '/', 302))

        response = self.client.post(
                '/meals/delete/' + self.meal2.slug + '/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/accounts/login/?next=/meals/delete/' +
                    self.meal2.slug + '/', 302))

    def test_index_auth(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/meals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['meals']), 3)
        self.assertEqual(response.context['meals'][0]['name'], 'apple')
        self.assertEqual(response.context['meals'][1]['name'], 'banana')
        self.assertEqual(response.context['meals'][2]['name'], 'cake')

    def test_index_auth(self):
        self.assertEqual(
                self.client.login(
                    username=self.user1.username,
                    password=self.password1),
                True)
        response = self.client.get('/meals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['meals']), 3)
        self.assertEqual(response.context['meals'][0].name, 'apple')
        self.assertEqual(response.context['meals'][1].name, 'banana')
        self.assertEqual(response.context['meals'][2].name, 'cake')
        self.client.logout()

    def test_view(self):
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get('/meals/view/' + self.meal4.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['meal'].name, self.meal4.name)
        self.assertEqual(set(response.context['meal'].tags.names()),
                set(self.meal4.tags.names()))
        self.client.logout()

    def test_update(self):
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get('/meals/edit/' + self.meal4.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].name, self.meal4.name)
        self.assertEqual(set(response.context['object'].tags.names()),
                set(self.meal4.tags.names()))
        response = self.client.post('/meals/edit/' + self.meal4.slug + '/',
                { 'rating': Meal.AVERAGE, 'url': '', 'description': 'new',
                    'tags': 'newtag1, newtag2' }, follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/meals/', 302))
        updated_meal = Meal.objects.get(slug=self.meal4.slug)
        self.assertEqual(updated_meal.rating, Meal.AVERAGE)
        self.assertEqual(updated_meal.url, '')
        self.assertEqual(updated_meal.description, 'new')
        self.assertEqual(set(updated_meal.tags.names()),
                set(['newtag1', 'newtag2']))
        self.client.logout()

    def test_create(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/meals/add/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/meals/add/',
                { 'name': 'another test meal', 'rating': Meal.GREAT,
                    'url': 'http://www.wonkabar.com/', 'description': 'foobar',
                    'tags': 'scrumdiddlyumptious' }, follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/meals/', 302))
        created_meal = Meal.objects.get(slug='another-test-meal')
        self.assertEqual(created_meal.rating, Meal.GREAT)
        self.assertEqual(created_meal.url, 'http://www.wonkabar.com/')
        self.assertEqual(created_meal.description, 'foobar')
        self.assertEqual(set(created_meal.tags.names()),
                set(['scrumdiddlyumptious']))
        self.client.logout()

    def test_delete(self):
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get('/meals/delete/' + self.meal1.slug + '/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/meals/delete/' + self.meal1.slug + '/',
                    follow=True)
        self.assertEqual(response.redirect_chain[0],
                (u'http://testserver/meals/', 302))
        with self.assertRaises(Meal.DoesNotExist):
            Meal.objects.get(slug=self.meal1.slug)
        self.client.logout()
