from rest_framework import serializers
from ..models import Subject,Course, Module
from ..models import Content

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True) # Then, you add a modules attribute to CourseSerializer to nest the ModuleSerializer serializer.
    # You set many=True to indicate that you are serializing multiple objects.
    #The read_only parameter indicates that this field is read-only and should not be included in any input to create or update objects.
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview','created', 'owner', 'modules']

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()
    
class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order', 'item']

    # In this code, you define a custom field by subclassing the RelatedField serializer
    # field provided by REST framework and overriding the to_representation()
    # method. You define the ContentSerializer serializer for the Content model and
    # use the custom field for the item generic foreign key.


# You need an alternative serializer for the Module model that includes its contents,
# and an extended Course serializer as well. Edit the api/serializers.py file and
# add the following code to it:

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']
class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug','overview', 'created', 'owner', 'modules']

