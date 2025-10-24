from rest_framework import viewsets, permissions
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
import logging

# ✅ Initialisation du logger
logger = logging.getLogger(__name__)


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

    def perform_create(self, serializer):
        category = serializer.save()
        logger.info(
            f"🟢 Nouvelle catégorie créée : {category.name} (ID: {category.id})"
        )

    def perform_update(self, serializer):
        category = serializer.save()
        logger.info(f"🟡 Catégorie mise à jour : {category.name} (ID: {category.id})")

    def perform_destroy(self, instance):
        logger.warning(f"🔴 Catégorie supprimée : {instance.name} (ID: {instance.id})")
        instance.delete()


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
            logger.info(
                f"👤 {user.username} consulte ses propres posts + ceux publiés."
            )
            return Post.objects.filter(author=user) | Post.objects.filter(
                published=True
            )
        logger.info("📰 Un utilisateur non authentifié consulte les posts publiés.")
        return Post.objects.filter(published=True)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        logger.info(f"🟢 Nouveau post créé : '{post.title}' par {post.author.username}")

    def perform_update(self, serializer):
        post = serializer.save()
        logger.info(
            f"🟡 Post mis à jour : '{post.title}' (Auteur: {post.author.username})"
        )

    def perform_destroy(self, instance):
        logger.warning(
            f"🔴 Post supprimé : '{instance.title}' par {instance.author.username}"
        )
        instance.delete()


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
        comment = serializer.save(author=self.request.user)
        logger.info(
            f"💬 Nouveau commentaire par {comment.author.username} sur le post ID {comment.post.id}"
        )

    def perform_update(self, serializer):
        comment = serializer.save()
        logger.info(
            f"🟡 Commentaire mis à jour (ID: {comment.id}) par {comment.author.username}"
        )

    def perform_destroy(self, instance):
        logger.warning(
            f"❌ Commentaire supprimé (ID: {instance.id}) par {instance.author.username}"
        )
        instance.delete()
