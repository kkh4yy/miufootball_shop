# main/urls.py
from django.urls import path
from . import views  # <-- ini kuncinya: kita impor modul views
from main.views import add_product_entry_ajax

app_name = "main"

urlpatterns = [
    # Home / daftar produk
    path("", views.show_main, name="show_main"),
    path("products/", views.product_list, name="product_list"),

    # CRUD Product (pilih salah satu: create_product ATAU add_product)
    path("products/add/", views.create_product, name="create_product"),
    # Kalau di views kamu adanya add_product, pakai baris ini dan hapus baris di atas:
    # path("products/add/", views.add_product, name="add_product"),

    path("products/<int:id>/", views.show_product, name="show_product"),
    path("products/<int:id>/detail/", views.product_detail, name="product_detail"),
    path("products/<int:id>/edit/", views.edit_product, name="edit_product"),
    path("products/<int:id>/delete/", views.delete_product, name="delete_product"),

    # Data delivery (XML/JSON)
    path("xml/", views.show_xml, name="show_xml"),
    path("json/", views.show_json, name="show_json"),
    path("xml/<int:id>/", views.show_xml_by_id, name="show_xml_by_id"),
    path("json/<int:id>/", views.show_json_by_id, name="show_json_by_id"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    # OPSIONAL: aktifkan hanya kalau DI views.py kamu memang ada fungsi employee
    # path("add_employee/", views.employee, name="add_employee"),

    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
]
