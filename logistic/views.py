from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import connections
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def company_code_check(company_code_value):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.company_code != company_code_value:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator






@login_required
@company_code_check("logistic")
def index(request):
    if request.method == "POST":
        if 'add_exhibition' in request.POST:

            event_name = request.POST.get('event_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            city = request.POST.get('city')
            venue = request.POST.get('veindexnue')
            host = request.POST.get('host')
            organizer = request.POST.get('organizer')
            sector = request.POST.get('sector')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            website = request.POST.get('website')


            with connections['logistic'].cursor() as cursor:
                cursor.execute("""
                    INSERT INTO exhibitions (event_name, start_date, end_date, city, venue, host, organizer, sector, phone, email, website)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [event_name, start_date, end_date, city, venue, host, organizer, sector, phone, email, website])




        if 'delete_exhibition' in request.POST:
            exhibition_id = request.POST.get('id')


            if exhibition_id and exhibition_id.isdigit():
                exhibition_id = int(exhibition_id)

                with connections['logistic'].cursor() as cursor:
                    cursor.execute("DELETE FROM exhibitions WHERE id = %s", [exhibition_id])

        if 'delete_user' in request.POST:
            user_id = request.POST.get('id')
            if user_id and user_id.isdigit():
                user_id = int(user_id)
                try:
                    with connections['logistic'].cursor() as cursor:
                        cursor.execute("DELETE FROM todos WHERE sender_id = %s", [user_id])
                        cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})



        return redirect(('index'))



    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM todos LIMIT 2")
        todos = cursor.fetchall()

        cursor.execute("""
    SELECT * 
    FROM payments 
    ORDER BY date DESC 
    LIMIT 2
""")

        payments = cursor.fetchall()


        today = timezone.now().date()
        cursor.execute("SELECT SUM(amount) FROM payments WHERE date = %s", [today])
        today_amount = cursor.fetchone()[0] or 0


        cursor.execute("SELECT SUM(amount) FROM payments")
        total_amount = cursor.fetchone()[0] or 0


        cursor.execute("SELECT * FROM exhibitions LIMIT 2")
        exhibitions = cursor.fetchall()


        cursor.execute("SELECT * FROM users LIMIT 3")
        user_list = cursor.fetchall()


    today_revenue = today_amount * 0.8
    total_revenue = total_amount * 0.8

    return render(request, 'index.html', {
        'user': request.user,
        'todos': todos,
        'payments': payments,
        'today_amount': today_amount,
        'today_revenue': today_revenue,
        'total_amount': total_amount,
        'total_revenue': total_revenue,
        'exhibitions': exhibitions,
        'users': user_list,

    })



@login_required
@company_code_check("logistic")
def all_payments(request):
    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM payments ORDER BY date DESC")

        payments = cursor.fetchall()

    return render(request,'all_payments.html',{'payments': payments})


@login_required
@company_code_check("logistic")
def all_todos(request):
    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM todos")

        todos = cursor.fetchall()
        user=request.user

    return render(request,'all_todos.html',{'todos': todos,'user':user})



@login_required
@company_code_check("logistic")
def all_exhibitions(request):
    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM exhibitions")

        exhibitions = cursor.fetchall()
        user=request.user

    return render(request,'all_exhibitions.html',{'exhibitions': exhibitions,'user':user})






@login_required
@company_code_check("logistic")
def all_users(request):
    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()
        user=request.user

    return render(request,'all_users.html',{'users': users,'user':user})



