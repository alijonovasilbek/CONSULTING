from django.shortcuts import redirect
from functools import wraps
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db import connections, DatabaseError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime

def company_code_check(company_code_value):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.company_code != company_code_value:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@csrf_exempt
@login_required
@company_code_check("telegram")
def index1(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)  # Read JSON body
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['telegram'].cursor() as cursor:
                if item_type == 'user':
                    cursor.execute("DELETE FROM users WHERE id = %s", [item_id])
                elif item_type == 'test':
                    cursor.execute("DELETE FROM test WHERE testID = %s", [item_id])
                elif item_type == 'participation':
                    cursor.execute("DELETE FROM participation WHERE participationID = %s", [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]


        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM test')
            test_count = cursor.fetchone()[0]

        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM participation')
            participation_count = cursor.fetchone()[0]

        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM users ORDER BY id DESC LIMIT 4')
            user_list = cursor.fetchall()


        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM test ORDER BY testID DESC LIMIT 4')
            test_list = cursor.fetchall()


        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM participation ORDER BY participationID DESC LIMIT 4')
            participation_list = cursor.fetchall()
        current_time=datetime.now()
        return render(request, 'index1.html', {
            'user_list': user_list,
            'test_list': test_list,
            'participation_list': participation_list,
            'user_count': user_count,
            'test_count': test_count,
            'participation_count': participation_count,
            'current_time': current_time,
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def get_all_users(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            user_list = cursor.fetchall()
            user = request.user

        return render(request, 'get_all_users.html', {'user_list': user_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_id = data.get('id')

            with connections['telegram'].cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE id = %s', [user_id])

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_all_tests(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM test')
            test_list = cursor.fetchall()
            user = request.user

        return render(request, 'get_all_tests.html', {'test_list': test_list, 'user': user})

    elif request.method == "POST" and request.POST.get('delete_test'):
        try:
            test_id = request.POST.get('id')

            with connections['telegram'].cursor() as cursor:
                cursor.execute('DELETE FROM test WHERE testID = %s', [test_id])

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_all_participations(request):
    if request.method == "GET":
        with connections['telegram'].cursor() as cursor:
            cursor.execute('SELECT * FROM participation')
            p_list = cursor.fetchall()
            user = request.user

        return render(request, 'get_all_participations.html', {'participation_list': p_list, 'user': user})

    elif request.method == "POST" and request.POST.get('delete_participation'):
        try:
            participation_id = request.POST.get('id')

            with connections['telegram'].cursor() as cursor:
                cursor.execute('DELETE FROM participation WHERE participationID = %s', [participation_id])

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)