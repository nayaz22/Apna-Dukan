from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,orderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# Create your views here.
MERCHANT_KEY='Enter your Marchant Key';

def index(request):
    allProds=[]
    procat=Product.objects.values('category')
    cat={item['category'] for item in procat}
    for cats in cat:
        prods=Product.objects.filter(category=cats)
        n = len(prods)
        nSlides= n//4 + ceil((n/4)-(n//4))
        allProds.append([nSlides,range(1,nSlides),prods])
    parms={'allprods':allProds}
    return render(request,'shop/l1.html',parms)


def searchMath(query,item):
    if query in item.product_name.lower() or query in item.category.lower() or query in  item.desc.lower():
        return True
    else:
        
        return False

def search(request):
    query=request.GET.get('search','')
    if query !="" and len(query)>2:
        allProds=[]
        procat=Product.objects.values('category')
        cat={item['category'] for item in procat}
        for cats in cat:
            prodtemp=Product.objects.filter(category=cats)
            prods=[item for item in prodtemp if searchMath(query,item)]
            n = len(prods)
            nSlides= n//4 + ceil((n/4)-(n//4))
            if len(prods)!=0:
                allProds.append([nSlides,range(1,nSlides),prods])
        parms={'allprods':allProds}
    else:
        msg=True
        parms={'msg':msg}

    return render(request, 'shop/search.html', parms)

def about(request):
    return render (request,'shop/about.html')


def contact(request):
    if request.method=="POST":
        print(request)
        name= request.POST.get('name','')
        email=request.POST.get('email','')
        cell=request.POST.get('cel','')
        country=request.POST.get('country','')
        textarea=request.POST.get('textarea','')
        tell=True;
        contact=Contact(name=name, email=email, cel=cell, country=country, textarea=textarea)
        contact.save()
        return render (request,'shop/contact.html',{'tell':tell})
    return render (request,'shop/contact.html')



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = orderUpdate.objects.filter(order_id=orderId)
                updates = []

                for item in update:

                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].itemsJson}, default=str)
                return HttpResponse(response)
            else:
                
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')


def pv(request,myid):
    products = Product.objects.filter(id=myid)
    
    
    return render(request, 'shop/product.html',{'product':products[0]})


def checkout(request):
    if request.method=="POST":
        itemsJson=request.POST.get('itemsJson')
        order_id=request.POST.get('order_id')
        name=request.POST.get('name')
        amount=request.POST.get('amount')
        email=request.POST.get('email')
        address=request.POST.get('add1') +" "+request.POST.get('add2')
        phone=request.POST.get('phone')
        state=request.POST.get('state')
        city=request.POST.get('city')
        zip_code=request.POST.get('zip_code')
        order=Orders(itemsJson=itemsJson, order_id=order_id, name=name, email=email, address=address,
            phone=phone, state=state, city=city, zip_code=zip_code,amount=amount)
        order.save()
        update=orderUpdate(order_id=order.order_id,update_desc="Order is placed");
        update.save()
        thanks=True
        ord_id=order.order_id
        # return render(request,'shop/checkout.html',{"thanks":thanks,"id":ord_id})


        # Requesting Paytm to transfer the amount to your account after payment by user
        # pip install pycryptodome
        
        param_dict={

        'MID':'Enter Your Marchant ID',
        'ORDER_ID':str(order.order_id),
        'TXN_AMOUNT':str(amount),
        'CUST_ID':email,
        'INDUSTRY_TYPE_ID':'Retail',
        'WEBSITE':'WEBSTAGING',
        'CHANNEL_ID':'WEB',
        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})

    return render(request,'shop/checkout.html')




@csrf_exempt
def handlerequest(request):
    # Paytm will send you post request here

    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]= form[i]
        if i == 'CHECKSUMHASH':
            checksum=form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print("Order Successful")
        else:
            print("Order Failure")
    return render(request, 'shop/paymentstatus.html',{'response':response_dict})

    # return HttpResponse('done')