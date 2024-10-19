from datetime import datetime

from django.shortcuts import redirect
from functools import wraps
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db import connections, DatabaseError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def company_code_check(company_code_value):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.company_code != company_code_value:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def service(request):
    return  render(request, 'service.html')


@csrf_exempt
@login_required
@company_code_check("service")
def service_all(request):
    if request.method == "DELETE":
        try:

            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'user':
                    cursor.execute('DELETE FROM "User" WHERE id = %s', [item_id])
                elif item_type == 'message':
                    cursor.execute('DELETE FROM "ContactMessage" WHERE id = %s', [item_id])
                elif item_type == 'profile':
                    cursor.execute('DELETE FROM "UserProfile" WHERE id = %s', [item_id])
                elif item_type == 'referral':
                    cursor.execute('DELETE FROM "Referral" WHERE id = %s', [item_id])
                elif item_type == 'referred':
                    cursor.execute('DELETE FROM "Referred" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    if request.method == "GET":


        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "ContactMessage" ORDER BY id DESC LIMIT 4')
            message_list = cursor.fetchall()

        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "User" ORDER BY id DESC LIMIT 4')
            user_list = cursor.fetchall()


        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "UserProfile" ORDER BY id DESC LIMIT 4')
            profile_list = cursor.fetchall()


        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "Referral" ORDER BY id DESC LIMIT 4')
            referral_list = cursor.fetchall()

        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "Referred" ORDER BY id DESC LIMIT 4;')
            referred_list = cursor.fetchall()


        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM "User"')
            user_count = cursor.fetchone()[0]

        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM "ContactMessage"')
            message_count = cursor.fetchone()[0]


        current_time=datetime.now()
        return render(request, 'service.html', {
            'user_list': user_list,
            'profile_list': profile_list,
            'referral_list': referral_list,
            'message_list': message_list,
            'referred_list': referred_list,
            'user_count': user_count,
            'message_count':message_count,
            'current_time':current_time

        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



@csrf_exempt
@login_required
@company_code_check("service")
@require_http_methods(["GET", "DELETE"])
def service_users(request):
    if request.method == "GET":
        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "User"')
            user_list = cursor.fetchall()
            user = request.user

        return render(request, 'service_users.html', {'user_list': user_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'user':
                    cursor.execute('DELETE FROM "User" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



@csrf_exempt
@login_required
@company_code_check("service")
@require_http_methods(["GET", "DELETE"])
def service_messages(request):
    if request.method == "GET":
        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT * FROM "ContactMessage" ')
            message_list = cursor.fetchall()
            user = request.user

        return render(request, 'service_messages.html', {'message_list': message_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'message':
                    cursor.execute('DELETE FROM "ContactMessage" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

from  requests import  request

@csrf_exempt
@login_required
@company_code_check("service")
@require_http_methods(["GET", "DELETE"])
def service_profiles(request):
    if request.method == "GET":
        with connections['service'].cursor() as cursor:
            cursor.execute('''SELECT p.id, u.username, p.prize_inviting, p.profile_picture
            FROM "UserProfile" p
            JOIN "User" u ON p.user_id = u.id''')
            profile_list = cursor.fetchall()
            user = request.user

        return render(request, 'service_profiles.html', {'profile_list': profile_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'profile':  # 'message' o'rniga 'userprofile' kiritildi
                    cursor.execute('DELETE FROM "UserProfile" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@csrf_exempt
@login_required
@company_code_check("service")
@require_http_methods(["GET", "DELETE"])
def service_referrals(request):
    if request.method == "GET":
        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT r.id, u.username, r.referral_code, r.created_at FROM "Referral" r JOIN "User" u ON r.user_id = u.id')
            referral_list = cursor.fetchall()
            user = request.user

        return render(request, 'service_referrals.html', {'referral_list': referral_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'referral':
                    cursor.execute('DELETE FROM "Referral" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@csrf_exempt
@login_required
@company_code_check("service")
@require_http_methods(["GET", "DELETE"])
def service_referreds(request):
    if request.method == "GET":
        with connections['service'].cursor() as cursor:
            cursor.execute('SELECT r.id , u.username, r.referred_by_id , r.date_invited FROM "Referred" r JOIN "User" u ON r.user_id = u.id')
            referred_list = cursor.fetchall()
            user = request.user

        return render(request, 'service_referreds.html', {'referred_list': referred_list, 'user': user})

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            item_type = data.get('type')
            item_id = data.get('id')

            if not item_type or not item_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid parameters.'})

            with connections['service'].cursor() as cursor:
                if item_type == 'referred':
                    cursor.execute('DELETE FROM "Referred" WHERE id = %s', [item_id])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid item type.'})

            return JsonResponse({'status': 'success', 'message': f'{item_type.capitalize()} deleted successfully!'})

        except DatabaseError as e:
            return JsonResponse({'status': 'error', 'message': 'Error deleting item: ' + str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

