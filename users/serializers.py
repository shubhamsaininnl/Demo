from __future__ import unicode_literals

import base64

from rest_framework import serializers

from users import models as users_models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.User
        fields = '__all__'
