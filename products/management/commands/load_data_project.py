

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Product, PCategory, PSubcategory, PBrand, ProductImage
from products import filters

# mys scripts folder for first update
from scripts.inits.load_users import load_users_init
from scripts.inits.load_orders import load_orders_init
from scripts.inits.load_store import load_store_init


# command python manage.py load_data_project
def clean_value(value, zero=False):
    """
        Cleans null or empty values and converts them to None or Zero as appropriate 
        for the database and stores them correctly.

    Args:
        value (any): The value obtained from the data source (e.g., an Excel file).
        zero (bool): Enables returning 0 instead of None for numeric fields.

    Returns:
        Returns a valid value or None or Zero as appropriate
    """
    result = None if pd.isna(value) or value == '' else value
    
    if zero:
        return 0 if result is None else result
    
    return result


class Command(BaseCommand):
    help = "To generically load all the necessary data for the models we created "
    help += "in this case, it includes loading Product models from Excel to the database. "
    help += "On the other hand, dictionaries were simply used to create model examples like Store, User, Orders"
        
    def handle(self, *args, **kwargs):
        
        # products = Product.objects.all()
        # if products.exists():
        #    print("This command was only for initial data load")
        #    return         

        # Path to the Excel file
        try:
            file = 'products/data/products_data.xlsx'
            
        except FileNotFoundError:
            print(f'File not found: {file}')
            return None
        
        # Get product data from the Excel file
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            name = clean_value(row.get("name"))
            
            if not name:
                print(f'Product "{index}" does not have a product_name.')
                continue
                
            category = clean_value(row.get("category"))
            subcategory = clean_value(row.get("subcategory"))
            brand = clean_value(row.get("brand"))
            
            # Create categories, subcategories, brands if they don't exist
            category_obj = None
            if category is not None:
                category_obj, _ = PCategory.objects.get_or_create(name=category)
                    
            sub_category_obj = None
            if subcategory is not None:
                sub_category_obj, created = PSubcategory.objects.get_or_create(name=subcategory, category=category_obj)
            
            brand_obj = None
            if brand is not None:
                brand_obj, _ = PBrand.objects.get_or_create(name=brand)
            
            # Get the rest of the values from the Excel
            price = clean_value(row.get("price"), zero=True)
            stock = clean_value(row.get("stock"), zero=True)
            discount = clean_value(row.get("discount"), zero=True)
            
            # Return true or false for availability
            available_str = row.get("available", "").lower()
            available = available_str in ["si", "sí", "yes"]

            description = clean_value(row.get("description"))
            image_url = clean_value(row.get("image_url"))
            image_url2 = clean_value(row.get("image_url2"))
            
            # Normalize the name before creating the product
            normalized_name = filters.normalize_or_None(name)
            slug = slugify(name)  # get the slugified version of the name
            
            # Retrieve or create the product
            product_obj, _ = Product.objects.get_or_create(
                name=name,
                slug=slug,
                normalized_name=normalized_name,
                price=price,
                stock=stock,
                discount=discount,
                available=available,
                category=category_obj,
                subcategory=sub_category_obj,
                brand=brand_obj,
                description=description,
            )
            
            # Add image URLs to the products
            cont = 0
            if image_url:
                ProductImage.objects.create(product=product_obj, image_url=image_url)
                cont += 1
        
            if image_url2:
                ProductImage.objects.create(product=product_obj, image_url=image_url2)
                cont += 1
             
            if created:
                print(f'Product {product_obj.name} created successfully with {cont} associated images.')
            else:
                print(f'Product {product_obj.name} updated successfully with {cont} associated images.')
             
        # ================================================================
        # Create other necessary data for the initial project load
        print("=" * 50)
        # This calls the function in scripts/ to load the initial orders
        load_orders_init()
        
        print("=" * 50)
        # This calls the function in scripts/ to load the initial Users
        load_users_init()
        
        print("=" * 50)
        # This calls the function in scripts/ to load the initial Store
        load_store_init()
