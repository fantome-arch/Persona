from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from . forms import createaccount
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import diaryform
from django.contrib.auth.decorators import login_required
from .models import Entry
from django.contrib.auth.hashers import check_password
from .models import User_Verification
import random
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .forms import verification_input
from .forms import forgotpassform
from .forms import password_reset_form1


def get_code():
    code=random.randint(000000,999999)
    return code

def home(r):
    if r.user.is_authenticated :
        check=User_Verification.objects.get(user=r.user)
        if check.is_verified:
            return redirect('/home/')
        else:
            return redirect('/verify/')
        
    
    else:
        return render(r,'home.html')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')

    else:
        if request.method=="POST":
            fm=createaccount(request.POST)
            if fm.is_valid():
                fm.save()
                verify_code=get_code()
                get_new_user=User.objects.get(username=fm.cleaned_data['username'])
                code=get_code()
                usr=User_Verification(user=get_new_user,verification_code=code,is_verified=False)
                usr.save()
                template=render_to_string('mail_body.html',{'name':usr.user,'code':usr.verification_code})
                recipient=str(get_new_user.email)
                email=EmailMessage(
                'Confirmation E-mail',
                 template,
                 settings.EMAIL_HOST_USER,
                 [recipient]

                )
                email.send()


                messages.success(request,'Your account has been created successfully please login and verify your e-mail')
                return redirect('login')
        else:
            fm=createaccount()
        return render(request,'signup.html',{'form':fm})


def user_login(request):
    if request.user.is_authenticated:
        check=User_Verification.objects.get(user=request.user)
        if check.is_verified:
            return HttpResponseRedirect('/home/')
        else:
            return redirect('/verify/')
        

    else:

        if request.method=='POST':
                fm=AuthenticationForm(request=request,data=request.POST)
                if fm.is_valid():
                    uname=fm.cleaned_data['username']
                    upass=fm.cleaned_data['password']

                    user=authenticate(username=uname,password=upass)

                    if user is not None:
                        login(request,user)

                        return HttpResponseRedirect('/home/')
                else:
                        error="The username or password is incorrect"
                        return render(request,'login.html',{'form':fm,'errors':error})
        else:
                fm=AuthenticationForm()
        return render(request,'login.html',{'form':fm})
        

        

def home2(request):
    if request.user.is_authenticated:
        check=User_Verification.objects.get(user=request.user)
        if check.is_verified:
            return render(request,'base.html')
        else:
            return redirect('/verify/')

    else:
        return redirect('/')

@login_required(login_url='login')  
def log_out(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def diary_entry(request):
    if request.user.is_authenticated :
        check=User_Verification.objects.get(user=request.user)
        if check.is_verified:
            if request.method=="POST":
                form=diaryform(request.POST)
                user=request.user
                if form.is_valid():
                    obj=form.save(commit=False)
                    obj.user=user
                    obj.save()
                    msg='Entry Added successfully'
                    print(obj.content)
                    return render(request,'entrypage.html',{'form':form,'message':msg})
            else:
                form=diaryform(request.POST)
           
        else:
            return redirect('/verify/')

            

        

        return render(request,'entrypage.html',{'form':form})

    else:
        return render(request,'home.html')


@login_required(login_url='login')
def view_entries_list(request,user,no=None):
    if request.user.is_authenticated :
        check=User_Verification.objects.get(user=request.user)
        if check.is_verified:
            usr=User.objects.get(username=user)
            if usr==request.user:
                entries=Entry.objects.filter(user=usr)
                if len(entries)==0:
                    noentry="Looks like you haven't written anything yet.Select 'Write an Entry' to write your first diary entry"
                else:
                    noentry=''
                if no is not None:
                    specific=Entry.objects.get(id=no)
                    viewingstate=True
                else:
                    specific="View your Entries"
                    viewingstate=False

            
                
                return render(request,'view_entry.html',{'entries':entries,'diaryentry':specific,'viewingstate':viewingstate,'noentry':noentry})
            
            else:
                usr=str(request.user)
                return redirect('/entry/'+usr)
        else:
            return redirect('/verify/')
    
    else:
            return redirect('/login')



@login_required(login_url='login')
def deleteentry(request,object) :
    if request.user.is_authenticated and request.user.is_active:
        deletable=Entry.objects.get(id=object)
        user_req=deletable.user
        if user_req==request.user:
            deletable.delete()
            user=str(request.user)
            return redirect('/entry/'+user)
    elif request.user.is_authenticated:
        return render(request,'verificationfail.html')


    

@login_required(login_url='login')
def updateentry(request,object):
    if request.user.is_authenticated and request.user.is_active:
        updateble=Entry.objects.get(id=object)
        user_req=updateble.user
        if user_req==request.user:
            if request.method=="POST":
                form=diaryform(request.POST,instance=updateble)
                user=request.user
                if form.is_valid():
                    obj=form.save(commit=False)
                    obj.user=user
                    obj.save()
                    msg='Entry Updated successfully'
                    userstr=str(user)
                    return redirect('/entry/'+userstr)
            else:
                form=diaryform(instance=updateble)
                return render(request,'entrypage.html',{'form':form})
        else:
            user_str=str(request.user)

            return redirect('/entry/'+user_str)
    elif request.user.is_authenticated:
        return render(request,'verificationfail.html')
            




def account_verification(request):
    if request.user.is_authenticated:
        get_user=User_Verification.objects.get(user=request.user)
        if get_user.is_verified==False:
            if request.method=="POST":
                input_field=verification_input(request.POST)
                if input_field.is_valid():
                    realcode=get_user.verification_code
                    if realcode==int(input_field.cleaned_data['verification_code']):
                        get_user.is_verified=True
                        get_user.save()
                        return redirect('/')
                    else:
                        error_msg="Incorrect code. Please check your e-mail or click resend to resend the code."
                        return render(request,'verificationfail.html',{'form':input_field,'error':error_msg})

            else:
                input_field=verification_input(request.POST)
                return render(request,'verificationfail.html',{'form':input_field})
        else:
            return redirect('/')
    else:
        return redirect('/login')                
        

    


    




def send_email(request):
    if request.user.is_authenticated:
        check=User_Verification.objects.get(user=request.user)
        if check.is_verified==False:
            newcode=get_code()
            check.verification_code=newcode
            check.save()
            template=render_to_string('mail_body.html',{'name':request.user,'code':newcode})
            recipient=str(request.user.email)
            email=EmailMessage(
                'Confirmation E-mail',
                 template,
                 settings.EMAIL_HOST_USER,
                 [recipient]

                )
            email.send()
            return redirect('/verify')
        else:
            return redirect('/')
    else:
        return redirect('/login')


def send_email_without_auth(email):
    try:
        get_user=User.objects.get(email__exact=email)
        check=User_Verification.objects.get(user=get_user)
        if check.is_verified==True:
            newcode=get_code()
            check.verification_code=newcode
            check.save()
            template=render_to_string('mail_body_reset.html',{'name':get_user.username,'code':newcode})
            recipient=str(email)
            email=EmailMessage(
                'Confirmation E-mail',
                 template,
                 settings.EMAIL_HOST_USER,
                 [recipient]

                )
            email.send()

    except:
        pass



def forgot_password(request):
    if request.method=="POST":
        form=forgotpassform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            send_email_without_auth(email)
            return redirect('/emailsent/'+str(email))

    else:
        form=forgotpassform(request.POST)
        return render(request,'forgot_password.html',{'form':form})



def pass_reset_email(request,email=None):
    if email is None:
        return redirect('/login')
    else:
        if request.method=="POST":
            form=password_reset_form1(request.POST)
            if form.is_valid():
                code=form.cleaned_data['verification_code']
                get_user=User.objects.get(email__exact=email)
                check=User_Verification.objects.get(user=get_user)
                if check.is_verified:
                    if check.verification_code==code:
                        newpass=form.cleaned_data['new_password']
                        confirmpass=form.cleaned_data['confirm_password']
                        if newpass==confirmpass:
                            get_user.set_password(str(newpass))
                            get_user.save()
                            return redirect('/login')
                        else:
                            message="Passwords don't match"
                            return render(request,'reset_pass.html',{'form':form,'msg':message})

                    else:
                        message='Incorrect code'
                        return render(request,'reset_pass.html',{'form':form,'message':message})

                else:
                    return render(request,'reset_error.html')

        else:
                form=password_reset_form1(request.POST)
                return render(request,'reset_pass.html',{'form':form})

            