import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import Product, Category

class Command(BaseCommand):
    help = "Seed database with sample products including images"

    def handle(self, *args, **kwargs):
        phones_cat, _ = Category.objects.get_or_create(name="Cell Phones")
        books_cat, _ = Category.objects.get_or_create(name="Books")

        products = [
            ("iPhone 14 Pro", "Apple iPhone 14 Pro with A16 Bionic chip", 999.99, phones_cat,
             "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone14pro-digitalmat-gallery-1-202209?wid=728&hei=686&fmt=jpeg&qlt=80&.v=1661027785750"),
            ("Samsung Galaxy S23", "Samsung Galaxy S23 with Snapdragon 8 Gen 2 processor", 849.99, phones_cat,
             "https://images.samsung.com/is/image/samsung/p6pim/levant/2202/gallery/levant-galaxy-s23-5g-s911-445943-sm-s911bzadhme-thumb-533658474?$216_216_PNG$"),
            ("Google Pixel 7", "Google Pixel 7 with Tensor G2 chip and Android 13", 599.99, phones_cat,
             "https://store.google.com/product/images/google-pixel-7-obsidian.jpg"),
            ("Atomic Habits", "James Clear’s book about building good habits and breaking bad ones.", 19.99, books_cat,
             "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg"),
            ("Clean Code", "Robert C. Martin’s classic book on writing clean, maintainable code.", 29.99, books_cat,
             "https://m.media-amazon.com/images/I/41jEbK-jG+L._SX374_BO1,204,203,200_.jpg"),
            ("Deep Learning with Python", "François Chollet’s book on deep learning using Keras and TensorFlow.", 39.99, books_cat,
             "https://m.media-amazon.com/images/I/71g2ednj0JL.jpg"),
        ]

        for name, desc, price, cat, img_url in products:
            if not Product.objects.filter(name=name).exists():
                product = Product(name=name, description=desc, price=price, category=cat)

                # download image
                response = requests.get(img_url)
                if response.status_code == 200:
                    file_name = img_url.split("/")[-1].split("?")[0]
                    product.image.save(file_name, ContentFile(response.content), save=True)

                product.save()

        self.stdout.write(self.style.SUCCESS("✅ Products with images seeded successfully!"))
