from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('blogs/', views.get_all_blogs, name='get_all_blogs'),
    path('blogs_admin/', views.get_admins_blogs, name='get_admins_blogs'),
    path('blog/<int:post_id>/', views.get_blog_details, name='get_blog_details'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog/delete/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('blog/edit/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('upload_image_endpoint/', views.upload_image, name='upload_image'),
    path('email_blog/<int:post_id>/', views.email_blog, name='email_blog'),
    path('blog/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),

]
