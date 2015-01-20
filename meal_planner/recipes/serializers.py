from recipes.models import Recipe
from rest_framework import serializers


class TagListSerializer(serializers.Field):
    """
    TagLists are serialized into lists of strings. Take not that the logic
    to translate a list of strings back into an updated tags field on the model
    is not implemented yet. At this point, a tag model field will only be
    usable in a read-only process using this serialization field.
    """
    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj

    def to_internal_value(self, data):
        if type(data) is not list:
            self.fail('incorrect_type', wrong_type=type(data).__name__)
        return data

    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected list, but got {wrong_type}'
    }


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='recipe-detail')
    tags = TagListSerializer()

    class Meta:
        model = Recipe
        fields = ('url', 'name', 'slug', 'rating',
                  'description', 'tags')
