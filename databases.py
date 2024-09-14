
from django.shortcuts import render
from django.db import connections

def postgres_users(request):
    with connections['base1'].cursor() as cursor:
        cursor.execute("SELECT id, username, email, first_name, last_name FROM public.user")
        rows = cursor.fetchall()
    with connections['base2'].cursor() as cursor:
        cursor.execute("SELECT id, username, email, first_name, last_name FROM public.user")
        rows1 = cursor.fetchall()
        print(rows1)
    return render(request, 'postgres_users.html', {'users': rows,'info':rows1})


