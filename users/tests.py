from __future__ import unicode_literals
import json

from django.shortcuts import reverse

from rest_framework.test import APITestCase

from users.models import User


class TestCreateApi(APITestCase):

    def setUp(self):
        self.user = User(
            first_name="Kallie",
            last_name="Blackwood",
            company_name="Rowley Schlimgen Inc",
            city="San Francisco",
            state="CA",
            zip=94104,
            email="kallie.blackwood@gmail.com",
            web="http://www.rowleyschlimgeninc.com",
            age=94
        )
        self.user.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_user_creation(self):
        response = self.client.post(reverse('users:user-list'), {
            "first_name": "Johnetta",
            "last_name": "Abdallah",
            "company_name": "Forging Specialties",
            "city": "Chapel Hill",
            "state": "NC",
            "zip": 27514,
            "email": "johnetta_abdallah@aol.com",
            "web": "http://www.forgingspecialties.com",
            "age": 27
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(201, response.status_code)

    def test_invalid_email(self):
        response = self.client.post(reverse('users:user-list'), {
            "first_name": "Johnetta",
            "last_name": "Abdallah",
            "company_name": "Forging Specialties",
            "city": "Chapel Hill",
            "state": "NC",
            "zip": 27514,
            "email": "johnetta_abdallah",
            "web": "http://www.forgingspecialties.com",
            "age": 27
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(400, response.status_code)


    def test_missing_field(self):
        response = self.client.post(reverse('users:user-list'), {
            'zipcode': '136128',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['email'], ['This field is required.'])


class TestRetrieveApi(APITestCase):

    def setUp(self):
        self.user = User(
            first_name="Kallie",
            last_name="Blackwood",
            company_name="Rowley Schlimgen Inc",
            city="San Francisco",
            state="CA",
            zip=94104,
            email="kallie.blackwood@gmail.com",
            web="http://www.rowleyschlimgeninc.com",
            age=94
        )
        self.user.save()

    def tearDown(self):
        User.objects.get(pk=self.user.id).delete()


    def test_getting_user(self):

        response = self.client.get(reverse('users:user-detail', kwargs={'pk': self.user.id}), format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual('Kallie', response.data["first_name"])

class TestUpdateApi(APITestCase):

    def setUp(self):
        self.user = User(
            first_name="Kallie",
            last_name="Blackwood",
            company_name="Rowley Schlimgen Inc",
            city="San Francisco",
            state="CA",
            zip=94104,
            email="kallie.blackwood@gmail.com",
            web="http://www.rowleyschlimgeninc.com",
            age=94
        )
        self.user.save()

    def tearDown(self):
        User.objects.get(pk=self.user.id).delete()

    def test_update_user(self):
        response = self.client.put(reverse('users:user-detail', kwargs={'pk': self.user.id}), {
            "first_name": "Shubham",
            "last_name": "Saini"
        }, format="json")

        self.assertEqual(200, response.status_code)
        user = User.objects.get(id=self.user.id)
        self.assertEqual('Shubham', user.first_name)


class TestDeleteApi(APITestCase):

    def setUp(self):
        self.user = User(
            first_name="Kallie",
            last_name="Blackwood",
            company_name="Rowley Schlimgen Inc",
            city="San Francisco",
            state="CA",
            zip=94104,
            email="kallie.blackwood@gmail.com",
            web="http://www.rowleyschlimgeninc.com",
            age=94
        )
        self.user.save()

    def test_deleting_user(self):
        response = self.client.delete(
            reverse('users:user-detail', kwargs={'pk': self.user.id}))

        self.assertEqual(200, response.status_code)

class TestUserListApi(APITestCase):

    def setUp(self):
        self.user = User(
            first_name="Kallie",
            last_name="Blackwood",
            company_name="Rowley Schlimgen Inc",
            city="San Francisco",
            state="CA",
            zip=94104,
            email="kallie.blackwood@gmail.com",
            web="http://www.rowleyschlimgeninc.com",
            age=94
        )
        self.user.save()

    def test_users_list(self):
        self.client.post(reverse('users:user-list'), {
            "first_name": "Johnetta",
            "last_name": "Abdallah",
            "company_name": "Forging Specialties",
            "city": "Chapel Hill",
            "state": "NC",
            "zip": 27514,
            "email": "johnetta_abdallah@aol.com",
            "web": "http://www.forgingspecialties.com",
            "age": 27
        })

        response = self.client.get(reverse('users:user-list'))
        self.assertEqual(2, response.data['count'])

        response = self.client.get("%s?name=Johnetta" % reverse('users:user-list'))
        self.assertEqual(1, response.data['count'])

        response = self.client.get("%s?sort=age" % reverse('users:user-list'))
        self.assertEqual(27, response.data['results'][0]['age'])

        response = self.client.get("%s?sort=-age" % reverse('users:user-list'))
        self.assertEqual(94, response.data['results'][0]['age'])
