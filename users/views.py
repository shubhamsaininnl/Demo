# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from users import models as users_models
from users import serializers as users_serializers


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class used for pagination on list page
    """
    page_size  = 5
    page_size_query_param = 'limit'


class CustomOrderingFilter(filters.OrderingFilter):
    ordering_param = 'sort'


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'name'


class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return the given User Details.

    create:
        Create a new User.

    destroy:
        Delete a User.

    update:
        Update a User.
    """

    queryset = users_models.User.objects.all()
    serializer_class = users_serializers.UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination

    filter_backends = (
        CustomOrderingFilter,
        CustomSearchFilter
    )
    search_fields = (
        'first_name',
        'last_name'
    )
    ordering_fields = ('age',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

