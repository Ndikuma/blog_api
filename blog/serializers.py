from rest_framework import serializers
from .models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""

    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""

    author_username = serializers.CharField(source="author.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "category",
            "category_name",
            "author",
            "author_username",
            "published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        """Automatically set the current user as the author"""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""

    author_username = serializers.CharField(source="author.username", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "post_title",
            "author",
            "author_username",
            "content",
            "created_at",
        ]
        read_only_fields = ["author", "created_at"]

    def create(self, validated_data):
        """Automatically set the current user as the author"""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
