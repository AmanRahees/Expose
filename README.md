
# Expose Ecommerce

Expose is an e-commerce web application that is built using Django and the front end using HTML, CSS and JavaScript. Expose has both email and OTP authentication moreover the guest user can also add
products to the cart but the user needs to log in if they want to checkout. The user can place the order using Cash on Delivery, Razorpay or Paypal as well as the user can see the order details and cancel the order.


## Live Demonstration
The E-commerce demo can be viewed online here: https://expose-shop.shop

## Getting Started
To get started you can simply clone this project repository and install the dependencies.

Clone the TryBasket repository using git:
```python
git clone https://github.com/AmanRahees/Expose.git
cd Expose
```

Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:
```python
(env) pip install -r requirement.txt
```

Once ```pip``` has finished downloading the dependencies:
```python
cd expose
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

And navigate to http://127.0.0.1:8000/
