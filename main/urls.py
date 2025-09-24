from django.urls import path
from .views import (
    show_main,
    create_product, 
    product_detail,
    show_xml, show_json,
    show_xml_by_id, show_json_by_id,
    add_product, product_list
)
app_name="main"
urlpatterns = [
    path('', show_main, name='show_main'),
    path("add/", create_product, name="create_product"),
    path("detail/<int:pk>/", product_detail, name="product_detail"),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<int:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path('products/add/', add_product, name="add_product"),
    path("products/", product_list, name="product_list"),
    path("products/<int:id>/", product_detail, name="product_detail"),
]