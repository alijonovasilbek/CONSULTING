from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connections, DatabaseError
from django.http import JsonResponse
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




@login_required()
@company_code_check("telegram")
def index1(request):
    if request.method == "POST" and request.POST.get('delete_user', False):
        user_id = request.POST.get('id')

        if user_id and user_id.isdigit():
            user_id = int(user_id)

            try:
                with connections['telegram'].cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE id = %s", [user_id])
                return JsonResponse({'status': 'success', 'message': 'User deleted successfully!'})
            except DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': 'Error deleting user: ' + str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid user ID.'})
        
    if request.method == "POST" and request.POST.get('delete_test', False):
        test_id = request.POST.get('id')

        if test_id and test_id.isdigit():
            test_id = int(test_id)


            try:
                with connections['telegram'].cursor() as cursor:
                    cursor.execute("DELETE FROM test WHERE id = %s", [test_id])
                return JsonResponse({'status': 'success', 'message': 'Test deleted successfully!'})
            except DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': 'Error deleting test: ' + str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid test ID.'})
        


    if request.method == "POST" and request.POST.get('delete_participation', False):
        p_id = request.POST.get('id')

        if p_id and p_id.isdigit():
            p_id = int(p_id)


            try:
                with connections['telegram'].cursor() as cursor:
                    cursor.execute("DELETE FROM participation WHERE id = %s", [p_id])
                return JsonResponse({'status': 'success', 'message': 'Participation deleted successfully!'})
            except DatabaseError as e:
                return JsonResponse({'status': 'error', 'message': 'Error deleting participation: ' + str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid participation ID.'})

    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM users LIMIT 3') 
            user_list = cursor.fetchall()
            user=request.user
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM test LIMIT 3')
            test_list = cursor.fetchall()
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM participation LIMIT 3')
            participation_list = cursor.fetchall()    


        return render(request, 'index1.html', {'user_list': user_list,'user': user, 'test_list': test_list, 'participation_list': participation_list})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




def get_all_users(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM users ') 
            user_list = cursor.fetchall()
            user=request.user

        return render(request, 'get_all_users.html', {'user_list': user_list, 'user': user})    
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def get_all_tests(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM test ') 
            test_list = cursor.fetchall()
            user=request.user

        return render(request, 'get_all_tests.html', {'test_list': test_list, 'user': user})    
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def get_all_participations(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM participation ') 
            p_list = cursor.fetchall()
            user=request.user

        return render(request, 'get_all_participations.html', {'participation_list': p_list, 'user': user})    
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})








