from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@require_http_methods(["GET", "DELETE"])
def consulting(request):
    if request.method == "GET":

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM public.user ORDER BY join_date DESC LIMIT 4")
            user_list = cursor.fetchall()


        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM about ORDER BY id DESC LIMIT 4")
            about_list = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM teammembership ORDER BY id DESC LIMIT 4")
            membership_list = cursor.fetchall()

        return render(request, 'consulting.html', {'users': user_list, 'abouts': about_list, 'memberships': membership_list})
    
    elif request.method == "DELETE":

        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'user':
                    cursor.execute("DELETE FROM public.user WHERE id = %s", [entity_id])
                elif entity_type == 'about':
                    cursor.execute("DELETE FROM public.about WHERE id = %s", [entity_id])
                elif entity_type == 'member':
                    cursor.execute("DELETE FROM public.membership WHERE id = %s", [entity_id])
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid entity type'})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
