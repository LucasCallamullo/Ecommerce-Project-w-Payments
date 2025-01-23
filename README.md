## Proyecto WebApp Ecommerce

### Description
This project is a fully functional Ecommerce WebApp developed with Django for the back-end and a responsive front-end using HTML, CSS (Bootstrap), and JavaScript. The application allows users to efficiently manage products and accounts through a CRUD system, with advanced features such as secure authentication and real-time content updates using AJAX.

[![Static Badge](https://img.shields.io/badge/Documentation-EN-blue)](https://github.com/LucasCallamullo/E-commerce-App-Web/blob/main/README.md) [![Documentation ES](https://img.shields.io/badge/Documentation-ES-green)](https://github.com/LucasCallamullo/E-commerce-App-Web/blob/main/README-ES.md)

### [EN]

### ⚙️ Technologies
| ![Python Badge](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white) | ![Django Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) | ![MySQL Badge](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white) | ![Pandas Badge](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
|:-:|:-:|:-:|:-:|


| ![HTML Badge](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![JavaScript Badge](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E) | ![CSS Badge](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | ![Bootstrap 5 Badge](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white) | 
|:-:|:-:|:-:|:-:|


### 🛠️ Tools 
| ![Git Badge](https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white) | [![GitHub Badge](https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)](https://github.com/LucasCallamullo) | ![VSCode Badge](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white) | ![DBeaver Badge](https://img.shields.io/badge/dbeaver-382923?style=for-the-badge&logo=dbeaver&logoColor=white)
|:-:|:-:|:-:|:-:|


#### Features
* RESTful API: Implemented with Django to handle all CRUD operations for cart, products, and users.
* Real-Time Updates: Utilization of AJAX for a seamless user experience, particularly in cart or login actions within the app.
* MySQL Database: Connection and data manipulation through Django's ORM.
* Deployment: The application is deployed on Railway, ensuring easy access and scalability.
* Responsive Interface: Adaptive design for different devices using HTML, CSS and Bootstrap 5.

Deploy On Railway: https://generic-ecommerce-project-production.up.railway.app

API Endpoints
List of the main API endpoints with a brief description of each.
Products Endpoint: CRUD operations for products.
Users Endpoint: CRUD operations for users

## API Endpoints

### Cart Endpoint
Estos endpoints están diseñados para ser utilizados a través de solicitudes AJAX en la aplicación:



# Principales Endpoints

- **POST /carrito/update/**: Endpoint AJAX para gestionar las acciones del carrito (agregar, reducir, eliminar productos). Devuelve un html renderizado si sale todo bien, sino mensajes de advertencia al usuario como que ya no queda stock, agrego un prodcuto o elimino el producto.
La solicitud debe incluir los detalles necesarios en el cuerpo:
  - **Datos del cuerpo de la solicitud:**
    - `producto_id` (int): ID del producto a agregar.
    - `value` (int): Cantidad del producto.
    - `action` (str): Acción a realizar (`add`, `less`, `remove`).
    - `cart_view` (str): Indica si se está en la vista del carrito (`true`, `false`).


- **GET /search-product/**: Endpoint AJAX para filtrar productos por nombre, category, subcategory o query por nombre asociada previamente. Responde con HTML para actualizar dinámicamente la interfaz de usuario. Los parámetros de filtro se obtienen con un metodo GET.

  - **Datos del cuerpo de la solicitud:**
      - `topQuery` (str): Cadena de búsqueda previa para los productos.
      - `categoryId` (int): ID de la categoría para filtrar.
      - `subCategoryId` (int): ID de la subcategoría para filtrar.
      - `inputNow` (str): Entrada actual para búsqueda en tiempo real. (3 lettras o más para activar)




### Otras Funcionalidades
La mayoría de las funcionalidades del sitio se renderizan directamente a través de vistas de Django, proporcionando una experiencia de usuario directa y sin interrupciones. Las operaciones CRUD para productos y usuarios se manejan a través de estas vistas.



#### Installation and Setup
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

