from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import connections
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def consulting(request):
    return render(request, 'consulting.html')


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






# @login_required
# @company_code_check("consulting")
def consulting(request):
    if request.method == "POST":
        if 'delete_user' in request.POST:
            user_id = request.POST.get('id')
            if user_id and user_id.isdigit():
                user_id = int(user_id)
                try:
                    with connections['consulting'].cursor() as cursor:
                        cursor.execute("DELETE FROM user WHERE id = %s", [user_id])
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})



        return redirect(('consulting'))
    
    with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM public.user ORDER BY join_date DESC LIMIT 2 ")
            user_list = cursor.fetchall()


   

    return render(request, 'consulting.html', {
        # 'user': request.user,
        'user_list': user_list,

    })



# @login_required
# @company_code_check("logistic")
# def all_payments(request):
#     with connections['logistic'].cursor() as cursor:
#         cursor.execute("SELECT * FROM payments ORDER BY date DESC")

#         payments = cursor.fetchall()

#     return render(request,'all_payments.html',{'payments': payments})


# @login_required
# @company_code_check("logistic")
# def all_todos(request):
#     with connections['logistic'].cursor() as cursor:
#         cursor.execute("SELECT * FROM todos")

#         todos = cursor.fetchall()
#         user=request.user

#     return render(request,'all_todos.html',{'todos': todos,'user':user})



# @login_required
# @company_code_check("logistic")
# def all_exhibitions(request):
#     with connections['logistic'].cursor() as cursor:
#         cursor.execute("SELECT * FROM exhibitions")

#         exhibitions = cursor.fetchall()
#         user=request.user

#     return render(request,'all_exhibitions.html',{'exhibitions': exhibitions,'user':user})






@login_required
@company_code_check("logistic")
def all_users(request):
    with connections['logistic'].cursor() as cursor:
        cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()
        user=request.user

    return render(request,'all_users.html',{'users': users,'user':user})



