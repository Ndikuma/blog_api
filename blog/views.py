from rest_framework import viewsets, permissions
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer


# ✅ Custom permission: only author can edit/delete
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow post authors to edit or delete their own posts.
    Others can only read.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only author can update or delete
        return obj.author == request.user


# ✅ Category management
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ✅ Post management
class PostViewSet(viewsets.ModelViewSet):
    """
    Manage blog posts.
    Authenticated users can create posts.
    Only authors can update/delete their own posts.
    """

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Show user’s posts + all published
            return Post.objects.filter(author=user) | Post.objects.filter(
                published=True
            )
        return Post.objects.filter(published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ✅ Comment management
class CommentViewSet(viewsets.ModelViewSet):
    """
    Manage comments on posts.
    Only authors can edit/delete their comments.
    """

    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
