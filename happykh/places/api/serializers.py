"""Serializers for model Place"""

from happykh.settings import HASH_IDS
from places.models import Place, Address, CommentPlace
from rest_framework import serializers
from users.api.serializers import UserSerializer
from users.backends import UserHashedIdField
from users.models import User
from utils import UploadedImageField, HashIdField


class AddressSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Address"""

    class Meta:
        model = Address
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    """
    Full ModelSerializer for model Place.
    All data should be passed with the same keys as attributes in the model!
    """

    user = UserHashedIdField()
    logo = UploadedImageField(max_length=None, )

    class Meta:
        model = Place
        fields = '__all__'

    def to_representation(self, instance):
        """Represent `address` as string """
        ret = super().to_representation(instance)
        ret['address'] = Address.objects.get(id=ret['address']).address
        return ret


class CommentPlaceSerializer(serializers.ModelSerializer):
    """
    Full ModelSerializer for model CommentPlace.
    Represents with creator's data.
    """

    class Meta:
        model = CommentPlace
        fields = '__all__'

    def to_representation(self, instance):
        """Representation data of comment and extended data of user"""
        ret = super().to_representation(instance)
        user_context = {
            'variation': User.thumbnail,
            'domain': self.context['domain']
        }
        comment_creator = User.objects.get(pk=instance.creator_id)
        creator_serializer = UserSerializer(comment_creator,
                                            context=user_context)
        ret['creator_image'] = creator_serializer.data['profile_image']
        ret['creator_fullname'] = comment_creator.get_full_name()
        ret['creator'] = HASH_IDS.encode(ret['creator'])
        return ret
