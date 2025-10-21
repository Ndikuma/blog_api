from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment
from faker import Faker
import random


class Command(BaseCommand):
    help = "Seed database with fake data (Users, Categories, Posts, Comments)"

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write(self.style.WARNING("🚀 Seeding data..."))

        # Optional: clear existing data
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Create users
        users = []
        for _ in range(20):
            user = User.objects.create_user(
                username=fake.user_name(), email=fake.email(), password="password123"
            )
            users.append(user)

        # Create categories
        categories = []
        for _ in range(20):
            category = Category.objects.create(name=fake.unique.word().capitalize())
            categories.append(category)

        # Create posts
        posts = []
        for _ in range(20):
            post = Post.objects.create(
                author=random.choice(users),
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=8),
                category=random.choice(categories),
                published=random.choice([True, False]),
            )
            posts.append(post)

        # Create comments
        for _ in range(20):
            Comment.objects.create(
                post=random.choice(posts),
                author=random.choice(users),
                content=fake.sentence(nb_words=15),
            )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
