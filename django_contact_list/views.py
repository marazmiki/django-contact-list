# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework import generics, serializers, fields, permissions
from django_contact_list.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=fields.CurrentUserDefault())

    class Meta(object):
        model = Contact
        fields = ['user', 'type', 'account']
        read_only_fields = ['link', 'text', 'html']


class ContactMixin(object):
    model = Contact
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ContactListView(ContactMixin, generics.ListCreateAPIView):
    pass


class ContactDetailView(ContactMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
