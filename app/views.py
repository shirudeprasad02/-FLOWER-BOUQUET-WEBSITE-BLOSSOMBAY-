from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from app.models import *
from django.db.models import Q
import razorpay
from django.core.mail import send_mail
# Create your views here.
# def hello(request):
#     print('hii')

# def ulogin(request):
#     context={}
#     if request.method == 'GET':
#         return render (request,'login.html')
#     else:
#         name=request.POST['uname']
#         password=request.POST['ppass']
      
#         # print(name)
#         # print(password)

#         u=authenticate(username=name,password=password)
#         print(u)
#         if u==None:
#             print('invalide credentials')
#             context['errmsg']='invalid credentials'
#             return render(request,'login.html',context)
#         else:
#             print('User login successfully')  
#             login(request,u)
            
#             return redirect('/index')
            
def ulogin(request):
    context={}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        name=request.POST['uname']
        password=request.POST['ppass']
        # print(name)
        # print(password)  
        u=authenticate(username=name,password=password)
        print(u)
        if u==None:
            print('invalide credentials')
            context['errmsg']='invalid credentials'
            return render(request,'login.html',context)
        else:
            print('User login successfully')  
            login(request,u)
            return redirect('/index')
        # return HttpResponse('Credentials checked')    


def register(request):
    context={}
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        name=request.POST['uname']    
        email=request.POST['uemail']
        password=request.POST['ppass']
        cpassword=request.POST['cppass']
        


        # print(name)
        # print(email)
        # print(password)
        # print(cpassword)

        if name=="" or email=="" or password=="":
            # print("Field can not be blank")
            context['errmsg']='Field can not be blank'
        elif password!=cpassword:
            # print("Password and Confirm password must be same")
            context['errmsg']='Password and Confirm password must be same'
        elif len(password)<6:
            # print("Password should be greater tha 8 character")     
            context['errmsg']='Password should be greater tha 8 character' 
        

        else:
            u=User.objects.create(first_name=name,username=email,email=email)
            u.set_password(password)
            u.save()
            u=User.objects.filter(username=email)
            print(u)
            t=Udetail.objects.create(uname=name,uid=u[0],pho=0)
            t.save()
            # return HttpResponse("Registered Successfully")
            # context['success']='User Registered Successfully'
            return redirect('/login')

        return render(request,'register.html',context)  

        # return HttpResponse('data')
        

    # return HttpResponse('Hello')

def ulogout(request):
    logout(request)
    return redirect('/index')


def index(request):
    # print(request.user.id)
    p=Flower.objects.filter(is_active=True)
    # print(p)
    context={}
    context['data']=p
    return render(request,'index.html')
    # return HttpResponse('hii')

def catfilter(request,cv):
    # print(cv)    
    q1=Q(cat=cv)
    q2=Q(is_active=True)    
    p=Flower.objects.filter(q1 & q2)
    # print(p)
    context={}
    context['data']=p
    return render(request,'redrose.html',context)   

def sort(request,sv):
    # print(sv)
    if sv=='1':
        # p=Product.object.order_by('-price').filter(is_active=True)
        t='-price'
    else:
        # p=Product.objects.order_by('+price').filter(is_active=True)  
        t='price'
    p=Flower.objects.order_by(t).filter(is_active=True)    
    context={}
    context['data']=p      
    return render(request,'index.html',context)    

def pricefilter(request):
    mn=request.GET['min']
    mx=request.GET['max']

    print(mn, '&' ,mx)
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    q3=Q(is_active=True)
    p=Flower.objects.filter(q1 & q2 &q3)
    context={}
    context['data']=p
    return render(request,'index.html',context)      

def search(request):
    s=request.GET['find']
    print(s)
    n=Flower.objects.filter(fname__icontains=s).filter(is_active=True)
    pd= Flower.objects.filter(flowert__icontains=s).filter(is_active=True)

    all=n.union(pd)
    context={}
    if len(all)==0:
        context['errmsg']='Product not found....'
        return render(request,'index.html',context)

    else:
        context['data']=all
        return render(request,'index.html',context)   

def product_detail(request,pid):
    # print(pid)
    p=Flower.objects.filter(id=pid)
    # print(p)
    context={}
    context['data']=p
    return render(request,'flowerdetail.html',context)     

def addtocart(request,pid):
    # print('product id is : ',pid)
    # print('athenticated user id user id is: ',request.user.id)
    context={}
    if request.user.is_authenticated:
        # print('user logged in')
        # u=request.user.id
        u=User.objects.filter(id=request.user.id)
        p=Flower.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        context['data']=p
        if len(c)!=0:
            context['errmsg']='Product Already Exist..!'
            return render(request,'flowerdetail.html',context)
        else:    
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added Successfully..!!"
            
            return render(request,'flowerdetail.html',context)
    else:
        # print('not logged in ')   
        return redirect('/login') 

    # return HttpResponse('fetched')  

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    context={}
    context['data']=c
    s=0
    for i in c:
        s=s+i.pid.price * i.qty  #s=s+i

    context['total']=s    
    context['n']=len(c)
    return render(request,'cart.html',context)   


def update(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    # print(type(x))
    if x=='1':  
        q=q+1
    elif q>1:
        q=q-1


    c.update(qty=q)    
    return redirect('/cart')

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')    

def detail(request):
    if request.method == 'GET':
        # print('1')
        c=Cart.objects.filter(uid=request.user.id)
        us=User.objects.filter(id=request.user.id)
        u=Udetail.objects.filter(uid=request.user.id)
        print(u)
        context={}
        if u[0].society != '' and u[0].area != '' and u[0].city != '' and u[0].pho != ''and u[0].uid != '' :
            print('from if')
            context['dataa']='datain'
        context['data']=c
        s=0
        for i in c:
            s=s+i.pid.price * i.qty  #s=s+i

        context['total']=s 
        context['e']=us[0].email   
        context['n']=len(c)
        context['u']=u
        print(u)
        # print(context)

        return render(request,'detail.html',context)
    else:
        so=request.POST['firstname']    
        ar=request.POST['lastname']
        cit=request.POST['city'] 
        mob=request.POST['mobile'] 

        print(so)
        print(ar)
        print(cit)
        print(type(mob))
        # u=User.objects.filter(id=request.user.id)
        t=Udetail.objects.filter(uid=request.user.id)
        t.update(society=so,area=ar,city=cit,pho=mob)
        print('1')
        # t.save()
        print('2')
        return redirect('/placeorder')      


def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    for i in c:
        a=i.pid.price * i.qty
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=a)
        o.save()
        i.delete()
    
    return redirect('/fetchorder')    
    # return HttpResponse("hii")
    # return redirect('/fetchorder')

def fetchorder(request):
    u=Udetail.objects.filter(uid=request.user.id)
    us=User.objects.filter(id=request.user.id)
    o=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=o
    s=0
    for i in o:
        s=s+i.amt
    context['dataa']=u
    context['e']=us[0].email
    context['total']=s
    context['n']=len(o)
    return render(request,'placeorder.html',context)     


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_Mi8Bm0hJfntbVk", "1Qx5GIlw7mlEC5AUMuSpv1GB"))

    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s + i.amt

    
    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)   
    # print(payment) 
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)     

def success(request):
    u=User.objects.filter(id=request.user.id)
    ud=Udetail.objects.filter(uid=request.user.id)
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt

    # print(u[0].name)
    # print(u[0].email)
    # print(ud[0].pho)
    # print(s)


    to=[u[0].email]
    
    sub='Payment Successful!'
    frm='prshirude03@gmail.com'
    msg='''Dear '''+u[0].first_name+''' 

    We are pleased to inform you that your payment of '''+str(s)+''' has
    been successfully processed. Thank you for your prompt payment.
    Amount: '''+str(s)+'''
    If you have any questions or need further assistance, please feel 
    free to contact our customer support team at '''+str(ud[0].pho)+'''.

    Thank you for your business!

    BlossomBay Team
    '''

    send_mail(
        sub,
        msg,
        frm,
        to,
        fail_silently=False
    )

    o=Order.objects.filter(uid=request.user.id)
    # print(c)
    for i in o:
        a=i.pid.price * i.qty
        h=History.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=a)
        h.save()
        i.delete()
    return render(request,'thankyou.html')    


def history(request):
    h=History.objects.filter(uid=request.user.id)
    return render(request,'order.html',{'data':h})

# def placeorder(request):
#     return HttpResponse('hii')        

def contact(request):
    return render(request,"contact.html")

def franchise(request):
    return render(request,"franchise.html")   

def carrer(request):
    return render(request,"carrer.html")       
    
def about(request):
    return render(request,'about.html')    

def terms(request):
    return render(request,'terms.html')    

def contact(request):
    if request.method == 'GET':
        return render(request,'contact.html')
    else:
        name=request.POST['fullname']    
        email=request.POST['uemail']
        phone=request.POST['phone']
        msg=request.POST['message']  

        # print(name)
        # print(email)
        # print(phone)
        # print(msg)

        c=Contact.objects.create(name=name,email=email,contact=phone,Message=msg)
        c.save()
        return redirect('/index')

    return render(request,'contact.html')  


     





 

