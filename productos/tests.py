from django.test import TestCase

# Create your tests here.
from productos.models import Product, PCategory, PSubcategory, PBrand, ProductImage

class ProductModelTest(TestCase):

    def setUp(self):
        # Crear datos de prueba para categorías, subcategorías y marcas
        self.category = PCategory.objects.create(name="Electronics")
        self.subcategory = PSubcategory.objects.create(name="Mobile Phones", category=self.category)
        self.brand = PBrand.objects.create(name="Samsung")

        # Crear un producto de prueba
        self.product = Product.objects.create(
            name="Samsung Galaxy S21",
            price=999.99,
            available=True,
            stock=50,
            discount=10,
            description="Latest Samsung Galaxy phone.",
            category=self.category,
            subcategory=self.subcategory,
            brand=self.brand
        )

    def test_product_creation(self):
        # Verificar que el producto fue creado correctamente
        self.assertEqual(self.product.name, "Samsung Galaxy S21")
        self.assertEqual(self.product.price, 999.99)
        self.assertTrue(self.product.available)
        self.assertEqual(self.product.stock, 50)
        self.assertEqual(self.product.discount, 10)
        self.assertEqual(self.product.description, "Latest Samsung Galaxy phone.")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.subcategory, self.subcategory)
        self.assertEqual(self.product.brand, self.brand)

    def test_product_str_method(self):
        # Verificar el método __str__ del producto
        self.assertEqual(str(self.product), "Samsung Galaxy S21")

    def test_category_relationship(self):
        # Verificar que el producto esté relacionado con la categoría correctamente
        self.assertEqual(self.product.category.name, "Electronics")
        self.assertEqual(self.product.subcategory.category.name, "Electronics")

    def test_invalid_category_subcategory_relation(self):
        # Verificar que el modelo lanza un error si la subcategoría no pertenece a la categoría
        with self.assertRaises(ValueError):
            invalid_category = PCategory.objects.create(name="Home Appliances")
            invalid_subcategory = PSubcategory.objects.create(name="Refrigerators", category=invalid_category)
            # Intentamos crear un producto con una relación inválida
            Product.objects.create(
                name="Samsung Refrigerator",
                price=499.99,
                available=True,
                stock=20,
                discount=15,
                description="Latest Samsung Refrigerator.",
                category=self.category,  # Esta categoría no coincide con la subcategoría
                subcategory=invalid_subcategory,
                brand=self.brand
            )

    def test_product_image_creation(self):
        # URL de la imagen que queremos probar
        image_url = "https://samsungar.vtexassets.com/arquivos/ids/191624/Samsung-99505726-ar-galaxy-s22-s901-sm-s901ezklaro-530921587Download-Source.png?v=638290108049600000"

        # Crear una imagen asociada al producto
        product_image = ProductImage.objects.create(
            product=self.product,
            image_url=image_url,
            main_image=True
        )

        # Verificar que la imagen se ha creado correctamente
        self.assertEqual(product_image.product, self.product)  # Verificar que el producto es el correcto
        self.assertEqual(product_image.image_url, image_url)  # Verificar que la URL de la imagen es correcta
        self.assertTrue(product_image.main_image)  # Verificar que es la imagen principal