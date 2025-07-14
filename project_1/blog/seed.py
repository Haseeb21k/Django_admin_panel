# blog/seed.py

from django.contrib.auth.models import User
from blog.models import Post, PostImage
from django.core.files.base import ContentFile
import random
from io import BytesIO
from PIL import Image

def create_users():
    usernames = ['alice', 'bob', 'charlie']
    for username in usernames:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password='test12345')
    print("Users created.")

def create_sample_image(name='demo.jpg'):
    image = Image.new('RGB', (300, 300), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name=name)

def create_posts():
    users = list(User.objects.all())
    for i in range(5):
        author = random.choice(users)
        post = Post.objects.create(
            title=f"Sample Post {i+1}",
            content="This is a test post generated for seeding.",
            author=author
        )

        # Optional: Add random number of images
        for j in range(random.randint(1, 3)):
            image_file = create_sample_image(name=f'post{i+1}_img{j+1}.jpg')
            PostImage.objects.create(post=post, image=image_file)

    print("Posts with images created.")
