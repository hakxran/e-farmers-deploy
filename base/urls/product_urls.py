from django.urls import path
from base.views import product_views as views


urlpatterns = [
    
    path("", views.getProducts, name="products"),
    
    path(
        "lowest-distance/",
        views.getFilteredProductLowestDistance,
        name="products-with-lowest-distance",
    ),
    path(
        "highest-points/",
        views.getFilteredProductHighestPoints,
        name="products-with-highest-points",
    ),
    path(
        "highest-price/",
        views.getFilteredProductHighestPrice,
        name="products-with-highest-price",
    ),
    path(
        "lowest-price/",
        views.getFilteredProductLowestPrice,
        name="products-with-lowest-price",
    ),
    path(
        "points_4_5_and_higher/",
        views.getFilteredProductWithPoints4_5AndHigher,
        name="products-with-points-4.5-Higher",
    ),
    path(
        "points_4/",
        views.getFilteredProductWithPoints4,
        name="products-with-points-4-Higher",
    ),
    path(
        "points_3_5_and_higher/",
        views.getFilteredProductWithPoints3_5AndHigher,
        name="products-with-points-3.5-Higher",
    ),
    path(
        "points_3/",
        views.getFilteredProductWithPoints3,
        name="products-with-points-3-Higher",
    ),
    path(
        "meyveler/",
        views.getProductsFruits,
        name="products-category-fruits",
    ),
    path(
        "sebzeler/",
        views.getProductsVegetables,
        name="products-category-vegatables",
    ),
    path(
        "kuruyemisler/",
        views.getProductsKuruyemis,
        name="products-category-kuruyemis",
    ),
    path(
        "sut-urunleri/",
        views.getProductsDairy,
        name="products-category-dairy",
    ),
    path(
        "et-tavuk-sarkutleri/",
        views.getProductsMeat,
        name="products-category-meat",
    ),
    path(
        "price-0-10/",
        views.getProductsPrice_0_10,
        name="products-category-price-0-10",
    ),
    path(
        "price-10-25/",
        views.getProductsPrice_10_25,
        name="products-category-price-10-25",
    ),
    path(
        "price-25-50/",
        views.getProductsPrice_25_50,
        name="products-category-price-25-50",
    ),
    path(
        "price-50-100/",
        views.getProductsPrice_50_100,
        name="products-category-price-50-100",
    ),
    path(
        "price-100-250/",
        views.getProductsPrice_100_250,
        name="products-category-price-100-250",
    ),
    path(
        "price-250-500/",
        views.getProductsPrice_250_500,
        name="products-category-price-250-500",
    ),
    path(
        "price-500-750/",
        views.getProductsPrice_500_750,
        name="products-category-price-500-750",
    ),
    path(
        "price-750-1000/",
        views.getProductsPrice_750_1000,
        name="products-category-price-750-1000",
    ),
    path(
        "price-1000/",
        views.getProductsPrice_gte_1000,
        name="products-category-price-1000",
    ),


    path("create/", views.createProduct, name="product-create"),
    path("upload/", views.uploadImage, name="image-uplaod"),
    path("farmers/", views.getFarmerProducts, name="farmer-products"),

    path("<str:pk>/reviews/", views.createProductReview, name="create-review"),
    path("<str:pk>/", views.getProduct, name="product"),

    path("update/<str:pk>/", views.updateProduct, name="product-update"),
    path("delete/<str:pk>/", views.deleteProduct, name="product-delete"),

    path("update/farmers/<str:pk>/", views.updateFarmersProduct, name="product-farmer-update"),
    path("delete/farmers/<str:pk>/", views.deleteFarmersProduct, name="product-farmer-delete"),
]
