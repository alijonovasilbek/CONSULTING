from django.utils import timezone
from functools import wraps
from django.shortcuts import render, get_object_or_404
from main.models import  User
from  ceo.forms import MessageFormAll,MessageForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import MessageForm
from main.models import Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required





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
@require_POST
def toggle_user_active(request):
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()


    active_user_count = User.objects.filter(is_active=True).count()
    inactive_user_count = User.objects.filter(is_active=False).count()

    return JsonResponse({
        'is_active': user.is_active,
        'active_user_count': active_user_count,
        'inactive_user_count': inactive_user_count
    })





@login_required
@company_code_check("ceo")
def ceo(request):
    users = User.objects.all()
    user_count = users.count()
    messages = Message.objects.all()
    messages_count = messages.count()
    active_user_count = User.objects.filter(is_active=True).count()
    inactive_user_count = User.objects.filter(is_active=False).count()

    return render(request, 'ceo.html', {
        'users': users,
        'user_count': user_count,
        'messages_count': messages_count,
        'active_user_count': active_user_count,
        'inactive_user_count': inactive_user_count
    })


@login_required
@company_code_check("ceo")
def send_message_all(request):
    if request.method == 'POST':
        form = MessageFormAll(request.POST)
        if form.is_valid():
            message_data = form.save(commit=False)
            message_data.sender = request.user


            all_users = User.objects.all()


            for user in all_users:
                message = Message(
                    sender=request.user,
                    receiver=user,
                    subject=message_data.subject,
                    body=message_data.body,
                    sent_at=timezone.now()
                )
                message.save()

            return redirect('message_list_ceo')
    else:
        form = MessageFormAll()

    return render(request, 'send_message_all.html', {'form': form})


@login_required
@company_code_check("ceo")
def send_message(request, receiver_id=None):
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
    else:
        receiver = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message_list_ceo')
    else:
        form = MessageForm(initial={'receiver': receiver})

    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})

from django.shortcuts import render


@login_required
def message_list(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    company_code = request.user.company_code
    return render(request, 'message_list.html', {
        'received_messages': received_messages,
        'company_code': company_code,
    })

@login_required
@company_code_check("ceo")
def message_list_ceo(request):
    received_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    return render(request, 'message_list_ceo.html', {'received_messages': received_messages})



@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    return render(request, 'message_detail.html', {'message': message})



@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)

    if request.method == 'POST':
        message.delete()
        return redirect('message_list')

    return redirect('message_detail', message_id=message_id)



@login_required
def delete_message_ceo(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)

    if request.method == 'POST':
        message.delete()
        return redirect('message_list_ceo')

    return redirect('message_detail', message_id=message_id)



@login_required
def user_dashboard(request, company_code):

    user = get_object_or_404(User, company_code=company_code, id=request.user.id)

    if user.company_code == 'telegram':
        return redirect('index1')
    elif user.company_code == 'ceo':
        return redirect('ceo')
    elif user.company_code == 'logistic':
        return redirect('index')
    elif user.company_code=='service':
        return  redirect('service_all')
    elif user.company_code == 'consulting':
        return redirect('consulting')
    else:
        return redirect('default_dashboard')
