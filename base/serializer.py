from rest_framework import serializers

# from django.contrib.auth.models import User  # AbstractUser Olabilir
from django.contrib.auth import get_user_model  # 1
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product,Order,OrderItem,ShippingAddress,Review

# PLEASE_NOTE_THIS PART !!!!!!!!!
# in order to create UserSerializer i used model = get_user_model() by importing 1 from the imports
# when i used model = User i got an error in the server
#'NoneType' object has no attribute '_meta' error to be exact



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isFarmer = serializers.SerializerMethodField(read_only=True)
    locationX = serializers.SerializerMethodField(read_only=True)
    locationY = serializers.SerializerMethodField(read_only=True)
    farmName = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ["id", "_id", "username", "email", "name", "isAdmin", "isFarmer","locationX","locationY",
        "farmName",
        "address",
        "description",
        "farmerPoint",
        "numReviews",
        "farmerPicture",
        "farmPicture",
        
        ]
        

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isFarmer(self, obj):
        return obj.isFarmer
   
    def get_locationX(self, obj):
        return obj.locationX
   
    def get_locationY(self, obj):
        return obj.locationY

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name

    def get_farmName(self, obj):
        return obj.farmName
    
    def get_address(self, obj):
        return obj.address
    
    def get_description(self, obj):
        return obj.description
    
    def get_farmerPoint(self, obj):
        return obj.farmerPoint
    
    def get_numReviews(self, obj):
        return obj.numReviews
    
    def get_farmPicture(self, obj):
        return obj.farmPicture
    
    def get_farmerPicture(self, obj):
        return obj.farmerPicture
    
    
      
    
   



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "_id",
            "username",
            "email",
            "name",
            "isAdmin",
            "isFarmer",
            "locationX",
            "locationY",
            "farmName",
            "address",
            "description",
            "farmerPoint",
            "numReviews",
            "token",
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
