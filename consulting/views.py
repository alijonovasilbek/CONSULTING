from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
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
@company_code_check("consulting")
@require_http_methods(["GET", "DELETE"])
def consulting(request):
    if request.method == "GET":

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM public.user ORDER BY join_date DESC LIMIT 4")
            user_list = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM public.user")
            total_users = cursor.fetchone()[0]

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM about ORDER BY id DESC LIMIT 4")
            about_list = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM teammembership ORDER BY id DESC LIMIT 4")
            membership_list = cursor.fetchall()
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM service_teammembership ORDER BY id DESC LIMIT 4")
            service_teammembership_list = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM service ORDER BY id DESC LIMIT 4")
            services= cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM conversation ORDER BY id DESC LIMIT 4")
            conversations = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM contactmessage ORDER BY id DESC LIMIT 4")
            messages = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM comment ORDER BY id DESC LIMIT 4")
            comments = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM blogpost ORDER BY id DESC LIMIT 4")
            blogposts = cursor.fetchall()

        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM blogpost")
            total_blogpost = cursor.fetchone()[0]

        user=request.user
        received_messages=user.received_messages.all().order_by('-sent_at')
        print(received_messages)




        return render(request, 'consulting.html',
        {'users': user_list, 'abouts': about_list, 'memberships': membership_list,
         'servicememberships': service_teammembership_list,'services': services,'conversations': conversations,
         'messages': messages, 'comments': comments,'blogposts': blogposts,'totalusers':total_users,'totalblogposts':total_blogpost,
         'received_messages':received_messages})
    
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
                    cursor.execute("DELETE FROM teammembership WHERE id = %s", [entity_id])
                elif entity_type == 'servicemember':
                    cursor.execute("DELETE FROM service_teammembership WHERE id = %s", [entity_id])
                elif entity_type == 'service':
                    cursor.execute("DELETE FROM service WHERE id = %s", [entity_id])
                elif entity_type == 'conversation':
                    cursor.execute("DELETE FROM conversation WHERE id = %s", [entity_id])
                elif entity_type == 'message':
                    cursor.execute("DELETE FROM contactmessage WHERE id = %s", [entity_id])
                elif entity_type == 'comment':
                    cursor.execute("DELETE FROM comment WHERE id = %s", [entity_id])
                elif entity_type == 'blogpost':
                    cursor.execute("DELETE FROM blogpost WHERE id = %s", [entity_id])
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid entity type'})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



@login_required
@company_code_check("consulting")
def consusers(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM public.user ORDER BY id DESC")
            user_list = cursor.fetchall()

        return render(request,'cons_users.html',{'users': user_list})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'user':
                    cursor.execute("DELETE FROM public.user WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
@company_code_check("consulting")
def consabouts(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM about ORDER BY id DESC")
            abouts = cursor.fetchall()

        return render(request,'cons_abouts.html',{'abouts': abouts})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'about':
                    cursor.execute("DELETE FROM about WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



@login_required
@company_code_check("consulting")
def consteammembership(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM teammembership ORDER BY id DESC")
            teammemberships = cursor.fetchall()

        return render(request,'cons_teammemberships.html',{'memberships': teammemberships})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'member':
                    cursor.execute("DELETE FROM teammembership WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



@login_required
@company_code_check("consulting")
def servicememberships(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM service_teammembership ORDER BY id DESC")
            service_teammembership = cursor.fetchall()

        return render(request,'cons_servicememberships.html',{'servicememberships': service_teammembership})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'servicemember':
                    cursor.execute("DELETE FROM service_teammembership WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



@login_required
@company_code_check("consulting")
def consservices(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM service ORDER BY id DESC")
            services = cursor.fetchall()

        return render(request,'cons_services.html',{'services': services})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'service':
                    cursor.execute("DELETE FROM service WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



@login_required
@company_code_check("consulting")
def consconversation(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM conversation ORDER BY id DESC")
            conversations = cursor.fetchall()

        return render(request,'cons_conversation.html',{'conversations': conversations})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'conversation':
                    cursor.execute("DELETE FROM conversation WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})





@login_required
@company_code_check("consulting")
def conscontactmessage(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM contactmessage ORDER BY id DESC")
            messages = cursor.fetchall()

        return render(request,'cons_contactmessage.html',{'messages': messages})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'message':
                    cursor.execute("DELETE FROM contactmessage WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
@company_code_check("consulting")
def conscomments(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM comment ORDER BY id DESC")
            comments = cursor.fetchall()

        return render(request,'cons_comments.html',{'comments': comments})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'comment':
                    cursor.execute("DELETE FROM comment WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
@company_code_check("consulting")
def consblogpost(request):
    if request.method == "GET":
        with connections['consulting'].cursor() as cursor:
            cursor.execute("SELECT * FROM blogpost ORDER BY id DESC")
            blogposts = cursor.fetchall()

        return render(request,'cons_blogposts.html',{'blogposts': blogposts})

    elif request.method == "DELETE":
        entity_type = request.GET.get('type')
        entity_id = request.GET.get('id')

        try:
            with connections['consulting'].cursor() as cursor:
                if entity_type == 'blogpost':
                    cursor.execute("DELETE FROM blogpost WHERE id = %s", [entity_id])

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



# @login_required
# @company_code_check("consulting")
# def consservicemembership(request):
#     if request.method == "GET":
#         with connections['consulting'].cursor() as cursor:
#             cursor.execute("SELECT * FROM service_teammembership ORDER BY id DESC")
#             service_teammemberships = cursor.fetchall()
#
#         return render(request,'cons_serviceteammembership.html',{'servicememberships': service_teammemberships})
#
#     elif request.method == "DELETE":
#         entity_type = request.GET.get('type')
#         entity_id = request.GET.get('id')
#
#         try:
#             with connections['consulting'].cursor() as cursor:
#                 if entity_type == 'servicemember':
#                     cursor.execute("DELETE FROM service_teammembership WHERE id = %s", [entity_id])
#
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
