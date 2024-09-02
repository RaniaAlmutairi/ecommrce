from django.shortcuts import render ,redirect
from django.http import HttpResponse , JsonResponse
from django.template import loader
from .models import storetype , itemsdetails ,items , cart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,LoginUserForm

# Create your views here.
def index(request):

    temp=loader.get_template('index.html')
    return HttpResponse(temp.render({'request':request}))

def listitems(request):
    p=items.objects.filter(st_id=2)
    temp=loader.get_template('listitems.html')
    return HttpResponse(temp.render({'items':p,'request':request}))
    
def details(request,id):
    temp=loader.get_template('details.html')
    d=itemsdetails.objects.select_related('items').filter(id=id).first()
    d.total=d.qty*d.items.price
    return HttpResponse(temp.render({'d':d,'request':request}))

@login_required(login_url='/auth_login/')
def checkout(request):
    temp = loader.get_template('checkout.html')
    return HttpResponse(temp.render({'request': request}))

@csrf_exempt
def add(request):
    id=request.POST.get('id')
    p= cart(itemsid=id)
    p.save()
    row=cart.objects.all()
    count = 0
    for item in row:
        count=count+1
    request.session["cart"]= count
    return JsonResponse({'count':count})


@csrf_exempt
def auth_login(request):
     form=LoginUserForm()
     if request.method=="POST":
          form=LoginUserForm(data=request.POST)
          if form.is_valid():
              username=form.cleaned_data['username']
              password=form.cleaned_data['password']
              print(username)

              user=authenticate(username=username,password=password)
              if user:
                   if user.is_active:
                        login(request,user)
                        return render(request,'checkout.html')
     context={'form':form}
     return render(request,'auth_login.html',context)

@csrf_exempt
def auth_register(request):
    template=loader.get_template('auth_register.html')
    form=CreateUserForm()
    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_login')
    context={'registerform': form}
    return HttpResponse(template.render(context=context))