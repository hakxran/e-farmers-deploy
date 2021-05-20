from django.urls import path
from base.views import product_views as views


urlpatterns = [
    
    path("", views.getProducts, name="products"),
    

    path("create/", views.createProduct, name="product-create"),
    path("upload/", views.uploadImage, name="image-uplaod"),
    path("farmers/", views.getFarmerProducts, name="farmer-products"),

    path("<str:pk>/reviews/", views.createProductReview, name="create-review"),
    path("<str:pk>/", views.getProduct, name="product"),

    path("update/<str:pk>/", views.updateProduct, name="product-update"),
    path("delete/<str:pk>/", views.deleteProduct, name="product-delete"),

    path("update/farmers/<str:pk>/", views.updateFarmersProduct, name="product-farmer-update"),
    path("update/farmers/<str:pk>/", views.deleteFarmersProduct, name="product-farmer-delete"),
]
