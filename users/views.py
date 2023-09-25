from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404
from . forms import RegistrationForm, UserForm, UserProfileForm,MessageForm
from . models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']



        #send email
        mail_subject = name + ' sent a message from your Website.'
        message = message
        from_email = email

        send_email = EmailMessage(mail_subject, message, from_email, to=['regmotech@gmail.com'])
        send_email.send()
        
        messages.success(request, name + ' your message has been sent. Thank you!')
   
    return render(request, 'contact.html')



def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('users/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Thank you for registering us. We have sent you a verification email to your email address')
            return redirect('/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your Account is Activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link!')
        return redirect('register')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password, is_active=True)

        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect(request.GET['next'] if 'next' in request.GET  else 'account')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return redirect('login')
    return render(request, 'users/login.html')


@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You Are Logged Out!')
    return redirect('login')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please Reset Your Password'
            message = render_to_string('users/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset has been sent to your email address')
            return redirect('login')


        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')

    return render(request, 'users/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
     
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password!')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link is expired!')
        return redirect('login')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successful')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match!')
            return render('resetpassword')
    else:
        return render(request, 'users/resetpassword.html')


@login_required(login_url='login')
def account(request):
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('account')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'users/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)

            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request, 'Password Updated Successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Current Password Incorrect!')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')

    context = {
     'userprofile': userprofile
        }
    return render(request, 'users/change_password.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.userprofile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.userprofile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)



@login_required(login_url='login')
def createMessage(request, pk):
    user = request.user
    if  user.is_admin == True:
        recipient = UserProfile.objects.get(id=pk)
        form = MessageForm()

        try:
            sender = request.user.userprofile
        except:
            sender = None

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = sender
                message.recipient = recipient
                message.save()

                messages.success(request, 'Your message was successfully sent!')
                return redirect('create-message', pk=recipient.id)

        context = {'recipient': recipient, 'form': form}
        return render(request, 'users/message_form.html', context)
        
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')
