from django.shortcuts import render,redirect
from django.views.generic import View
from ToDo_App.forms import registerform,signin,taskform
from ToDo_App.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.

#Decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you should login first")
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper  



def mylogin(fn):
  def wrapper(request,*args,**kwargs):
      id=kwargs.get('pk')
      data=Task.objects.get(id=id)
      if  data.user!=request.user:
          return redirect('login')
      else:
          return fn(request,*args,**kwargs)
  return wrapper                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
 
#signup 

class signupView(View):
    def get(self,request,*args,**kwargs):
        form=registerform()
        return render(request,"reg.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=registerform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print(form.cleaned_data)
        form=registerform()
        # else:
        #     print("getout")
        return redirect('login')


 #Signin   

class signinview(View):
    def get(self,request,*args,**kwargs):
        form=signin()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=signin(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            print(u_name,pswd)
            user_obj=authenticate(request,username=u_name,password=pswd)
            if user_obj:
                print("valid")
                login(request,user_obj)
                return redirect('add')
            else:
                print("invalid")
            return render(request,"signin.html",{"form":form})

# Add Tasks
        
@method_decorator(signin_required,name='dispatch')

class taskadd(View):
    def get(self,request,*args,**kwargs):
        form=taskform()
        return render(request,'add.html',{"form":form}) 
    def post(self,request,*args,**kwargs):
        form=taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('task')           
        else:
            print("get out")
            return render(request,"add.html",{"form":form})
        

# Table list 
               
@method_decorator(signin_required,name='dispatch')

class taskview(View):
    def get(self,request,*args,**kwargs):
        data=Task.objects.filter(user=request.user).order_by('Complete')
        return render(request,"index.html",{"data":data})          
    def post(self,request,*args,**kwargs):
            data=Task.objects.filter(user=request.user).order_by('Complete')
            return render(request,"index.html",{"data":data})               

# SignOut
    
class signout(View):
    def get(self,request):
        logout(request)
        return redirect("login")
    

#http://127.0.01.8000/task/edit/<int:pk>
    
@method_decorator(signin_required,name='dispatch')
@method_decorator(mylogin,name='dispatch')

#update
class Taskupdate(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk") 
        data=Task.objects.get(id=id)
        if data.Complete == False:
            data.Complete = True
            data.save()
        elif data.Complete == True:
            data.Complete = False
            data.save()
        return redirect('task') 
      
#http://127.0.01.8000/task/delete/<int:pk>

@method_decorator(signin_required,name='dispatch')
@method_decorator(mylogin,name='dispatch')

#delete
class taskdelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Task.objects.filter(id=id).delete()
        return redirect('task')   
     
#user delete
    
class user_del(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        User.objects.get(id=id).delete()
        return redirect('reg')



