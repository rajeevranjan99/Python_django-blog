from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # Includes all fields from the Post model

    def __init__(self, *args, **kwargs):
        """Dynamically filter fields if 'fields' parameter is provided"""
        fields = kwargs.pop('fields', None)
        super(PostSerializer, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
