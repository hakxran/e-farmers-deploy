from django.shortcuts import render
import pyqrcode,io,qrcode
from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import boto3
from botocore.exceptions import NoCredentialsError
import os


from django.db import connection


from base.models import Product, Order , OrderItem, ShippingAddress,Box,BoxDelivery,ShipmentCompany,DirectDelivery
from django.contrib.auth import get_user_model
from base.serializer import (
    ProductSerializer,
    OrderSerializer,
    UserSerializer,
    OrderBoxSerializer
)


from rest_framework import status
from datetime import datetime

ACCESS_KEY = 'AKIA3R6YNNJFEWCZNPNK'
SECRET_KEY = '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'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    company = ShipmentCompany.objects.get(_id=1)
    selectedBox = Box.objects.get(_id=1)

    orderItems = data['orderItems']

    if orderItems and len(orderItems)== 0 :
    
        return Response({'detail':'No Order Items'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        #(1)Create Order
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        ###
        #(2) Create Shipping Adress
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
            isBoxDelivery=data['shippingAddress']['isBoxDelivery'],
            
        )

        #(3) Create order items and ser order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['count'],
                price=i['unitPrice'],
                image=product.image.url,

            )
            #(4) Update stock
            product.countInStock -= item.qty
            product.save()

    #(5)Create Box Delivery or DirectDelivery
    if data['shippingAddress']['isBoxDelivery'] == True:
        company = ShipmentCompany.objects.get(_id=1)
        selectedBox = Box.objects.get(_id=1)
        boxDelivery = BoxDelivery.objects.create(
            shippingAddress=shipping,
            shipmentCompany=company,
            user=user,
            box=selectedBox,
        )
        boxDelivery.save()

    else:
        directDel = DirectDelivery.objects.create(
            shippingAddress=shipping,
            shipmentCompany=company,
        )
        



    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getQrIdForBox(request,pk):
   
    try:
        orders = Order.objects.get(_id=pk)
        return Response("True")
            
    except:
        return Response("False")

   

"""@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFarmersOrders(request):
    user = request.user
    farmerUser = UserSerializer(user, many=False)
    
    #Order.orderItem_set.all()
    
    #Order      where order.id = OrderItem.orderid and orderItem.productId = product.id and product.user = user.userid and user=userıd
    #orderUsers = get_user_model().objects.get(id=user.id)
    #orderUsers.
    
    #query1= OrderItem.objects.all()
    
    #orders = Order.objects.filter(Q(_id_contains=query1) | Q(last_name__contains=query)

    productFilter=user.product_set.all()
    orderItem= OrderItem.objects.filter()
    orders = Order.objects.filter(user_id=user.id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)"""

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFarmersOrders(request):
    user = request.user
    farmerUser = UserSerializer(user, many=False)
    orders = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT base_order._id FROM base_order,base_orderitem,base_product,base_user WHERE base_order._id = base_orderitem.order_id AND base_orderitem.product_id = base_product._id AND base_product.user_id = base_user.id AND base_user.id = %s",
            [user.id],
        )
        farmerOrder = cursor.fetchone()
        for i in farmerOrder:
            order = Order.objects.get(_id=i)
            orders.append(order)
           
       
        serializer = OrderSerializer(orders, many=True)
        
        
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail':'Not authorized to view this order'}, status = status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail':'Order does not exist'},status = status.HTTP_400_BAD_REQUEST)

    
'''
@api_view(['GET'])#delete all
def createqr(request):
    #user = request.data
    #serializer = UserSerializer(user, many=False)
    a = "12345678"
    x = a + ".png"
    qr = pyqrcode.create(a)
    qr.png(x, scale=8)
    #z=Image.open("12345.png")
    uploaded = upload_to_aws(x, 'efarm-bucket', x)
   
    #qr.png(x, scale=8)
    #user.farmPicture = contents
    #product_id = data['product_id']
    product = Product.objects.get(_id=5)

    

    #client = boto3.client('s3', region_name='us-west-2')
    #client.upload_file('1234.png', 'efarm-bucket', '1234.jpg')
    #product.image = request.FILES.get('image')
    product.image = x
    product.save()
    os.remove(x) 
    #user.save()
    return Response('Image was uploaded')
    ''' 

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    a = str(pk)
    x = a + ".png"
    order.orderqr=x
    qr = pyqrcode.create(a)
    qr.png(x, scale=8)
    uploaded = upload_to_aws(x, 'efarm-bucket', x)
    
    order.isPaid = True
    order.paidAt = datetime.now()
    

    

    #order.totalPrice
    order.save()
    os.remove(x) 

    return Response('Order was paid')

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')