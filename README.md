## Proyecto WebApp Ecommerce

### Description
This project is a fully functional Ecommerce WebApp developed with Django for the back-end and a responsive front-end using HTML, CSS (Bootstrap), and JavaScript. The application allows users to efficiently manage carts, products and accounts through a CRUD system, real-time content updates using AJAX. Additionally, the use of Pandas and Excel simplifies the initial loading of product data, allowing for quick and efficient setup by importing product details directly from Excel files, making it easy to have a fully functional page with minimal effort.

[![Static Badge](https://img.shields.io/badge/Documentation-EN-blue)](https://github.com/LucasCallamullo/generic-ecommerce-project/blob/main/README.md) [![Documentation ES](https://img.shields.io/badge/Documentation-ES-green)](https://github.com/LucasCallamullo/generic-ecommerce-project/blob/main/README-es.md)

### [EN]

### ⚙️ Technologies
#### Back-End
| ![Python Badge](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white) | ![Django Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) | ![DRF Badge](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) | ![MySQL Badge](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white) | ![Pandas Badge](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
|:-:|:-:|:-:|:-:|:-:|


#### Fornt-End
| ![HTML Badge](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![JavaScript Badge](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E) | ![CSS Badge](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | ![Bootstrap 5 Badge](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white) | 
|:-:|:-:|:-:|:-:|


### 🛠️ Tools 
| ![Git Badge](https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white) | [![GitHub Badge](https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/LucasCallamullo) | ![Postman Badge](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white) | ![DBeaver Badge](https://img.shields.io/badge/dbeaver-382923?style=for-the-badge&logo=dbeaver&logoColor=white)
|:-:|:-:|:-:|:-:|


#### Features
* RESTful API: Implemented with Django to handle all CRUD operations for cart, products, and users.
* Real-Time Updates: Utilization of AJAX for a seamless user experience, particularly in cart or login actions within the app.
* MySQL Database: Connection and data manipulation through Django's ORM.
* Deployment: The application is deployed on Railway, ensuring easy access and scalability.
* Responsive Interface: Adaptive design for different devices using HTML, CSS and Bootstrap 5.

#### Deploy
| ![Railway Badge](https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white) |
|:-:|
Deploy On Railway: https://generic-ecommerce-project-production.up.railway.app

<br></br>

## API Main Endpoints

- **POST /carrito/update/**: AJAX endpoint to manage cart actions (add, reduce, remove products). Returns rendered HTML if successful; otherwise, it shows warning messages to the user such as out of stock, product added, or product removed. The request must include the following details in the body:
  - **Request body data:**
    - `producto_id` (int): ID of the product to add.
    - `value` (int): Quantity of the product.
    - `action` (str): Action to perform (`add`, `less`, `remove`).
    - `cart_view` (str): Indicates if the user is on the cart view (`true`, `false`).

- **GET /search-product/**: AJAX endpoint to filter products by name, category, subcategory, or previous search query. Responds with HTML to dynamically update the user interface. Filter parameters are retrieved using the GET method.
  - **URL parameters:**
    - `topQuery` (str): Previous search string for products.
    - `categoryId` (int): Category ID to filter by.
    - `subCategoryId` (int): Subcategory ID to filter by.
    - `inputNow` (str): Current input for real-time search (activated with 3 or more letters).

## Other Functionalities
Most of the site's functionalities are rendered directly through Django views, providing a seamless and uninterrupted user experience. CRUD operations for products and users are handled through these views.

## Installation and Setup
1. **Clone the repository:**:
   ```bash
   git clone https://github.com/LucasCallamullo/generic-ecommerce-project.git
   cd Generic-E-Commerce

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Apply Migrations: Run the migrations to create the tables in the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

4. **Run the load_data Script: This command will load initial data into your database using pandas and openpyxl**
   ```bash
   python manage.py load_data_project


### [ES]
[![Documentation ES](https://img.shields.io/badge/Documentation-ES-green)](https://github.com/LucasCallamullo/E-commerce-App-Web/blob/main/README-ES.md)

### Images:
![](https://i.pinimg.com/736x/73/5b/6e/735b6ebb2cf852e28472a2efcc378e9e.jpg)
![](https://i.pinimg.com/736x/e1/1b/8a/e11b8a41f2f803cb0bcbcc735b4fcbbf.jpg)

> Some screens of the app

<br></br>

### 💻 Contact Back-End Developer / Full-Stack Developer:
| [![GitHub Badge](https://img.shields.io/badge/github-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/LucasCallamullo) | [![LinkedIn Badge](https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lucas-callamullo/) | [![Youtube Badge](https://img.shields.io/badge/YouTube%20-%23FF0000.svg?&style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@lucas_clases_python) |
|:-:|:-:|:-:|

| **Lucas Callamullo** |
|:-:|

