from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages
import jwt

def jasonWebToken(username):
  payload_data = {
    "username": username  
  }
  token = jwt.encode(
    payload=payload_data,
    key='bubble_tea_project123&'
  )
  return(token)

def decode_user(token):
   decoded_data = jwt.decode(jwt=(token), key='bubble_tea_project123&', algorithms=['HS256'],options={'verify_signature': False}) 
   return decoded_data

def signup(request):
  
  if request.method == 'POST':

    name = request.POST.get('name', '')
    surname = request.POST.get('surname', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    cursor = connection.cursor()
    exist = cursor.execute("SELECT username FROM customer WHERE username = %s", params=[username])

    if exist != 0:
      messages.error(request, 'Username already exist.')
      return redirect('../signup')
    else:
      cursor.execute("INSERT INTO customer (name, surname, username, password) VALUES (%s, %s, %s, %s)", params=[name, surname, username, password])

    return redirect('../login')
  else:
    return render(request, 'signup.html')



def login(request):
  # if len(request.session['usertoken']) > 0:
  if request.method == 'POST':

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    print(username, password)

    cursor = connection.cursor()
    usernameFound = cursor.execute("SELECT username FROM customer WHERE username = %s", params=[username]) 
    passwordFound = cursor.execute("SELECT password FROM customer WHERE password = %s", params=[password])
    
    if usernameFound == 0 or passwordFound == 0:
      messages.error(request, 'Username or Password is wrong.')
      return redirect('../login')
    else:
      token = jasonWebToken(username)
      request.session["usertoken"] = token
      return redirect("../index")
  else:
    return render(request, 'login.html')
  


def home(request):
  try:
    usertoken = decode_user(request.session['usertoken'])
    username = usertoken['username']
    with connection.cursor() as cursor:
      cursor.execute('SELECT customer_id from customer WHERE username = %s', params=[username])
      result = dictfetchall(cursor)
      user_id = (result[0]['customer_id'])
    if len(request.session['usertoken']) > 0:
      if request.method == "GET":
        with connection.cursor() as cursor:
          cursor.execute("SELECT base_id, description as base from drink_base")
          bases = dictfetchall(cursor)
          
          cursor.execute("SELECT flavour_id , description as flavour from drink_flavour")
          flavours = dictfetchall(cursor)
          
          cursor.execute("SELECT popping_id, description as popping from drink_popping")
          poppings = dictfetchall(cursor)
        return render(request, 'home.html', { 'flavours' : flavours, 'bases' : bases, 'poppings' : poppings})
        
      if request.method == "POST":
        form = request.POST
        base = form['base']
        flavour = form['flavour']
        popping = form['popping']
        sugar = form['sugar']
        size = form['size']
        print(size)
        price = 5
        print(price)
        if size == "1" :
          price = 5
        elif size == "2" :
          price = 7
        elif size == "3" :
          price = 8
        print(price)
        with connection.cursor() as cursor:
          cursor.execute('INSERT INTO product (customer_id, base_id, flavour_id, popping_id, sugar, size, price, purchase_date) VALUES(%s,%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)', params=[ user_id, base, flavour, popping, sugar, size, price])
        return redirect('../index')
  except:
    return redirect('../login')

    
def profile(request):
    usertoken = decode_user(request.session['usertoken'])
    username = usertoken['username']
    with connection.cursor() as cursor:
        cursor.execute('SELECT * from customer WHERE username = %s', params=[username])
        result = dictfetchall(cursor)
        user_id = (result[0]['customer_id'])
        name = (result[0]['name'])
        surname = (result[0]['surname'])
        password = (result[0]['password'])
        myUser = {
           'username' : username,
           'name' : name,
           'surname' : surname,
           'password' : password,
        }
    if request.method == "GET":
        return render(request, 'profile.html', { 'myUser': myUser })
    if request.method == "POST" :
        form = (request.POST)
        name = form['name']
        surname = form['surname']
        password = form['password']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customer SET name=%s, surname=%s, password=%s WHERE customer_id = %s", [name, surname, password, user_id])
            messages.success(request, 'Profile edited!')
        return redirect('../profile')


def cookie(request):
  try:
    if len(request.session['usertoken']) > 0:
      print(request.session["usertoken"])
      return render(request, 'cookie.html', {"username": request.session["usertoken"]})
    else: 
      return redirect('../login')
  except:
    return redirect('../login')

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def index(request):
    try :
        if request.method == "GET":
          usertoken = decode_user(request.session['usertoken'])
          username = usertoken['username']
          with connection.cursor() as cursor:
              cursor.execute('SELECT customer_id from customer WHERE username = %s', params=[username])
              result = dictfetchall(cursor)
              user_id = (result[0]['customer_id'])
          with connection.cursor() as cursor:
              cursor.execute('SELECT drink_flavour.description as flavour, drink_popping.description as popping, drink_base.description as base, product.price, product.size, product.purchase_date as date FROM product JOIN customer ON product.customer_id = customer.customer_id JOIN drink_flavour ON product.flavour_id = drink_flavour.flavour_id JOIN drink_popping ON product.popping_id = drink_popping.popping_id JOIN drink_base ON product.base_id = drink_base.base_id WHERE product.customer_id = %s ORDER BY product.purchase_date desc LIMIT 5', params=[user_id])
              orders = dictfetchall(cursor)
          myUser = {'username' : username , 'user_id' : user_id}
          return render(request, 'index.html',{'myUser': myUser, 'orders': orders})
    except KeyError :
        return redirect('../login')
    
def logout(request):
   if request.method == "GET":
      del request.session['usertoken']
      return redirect('../login')