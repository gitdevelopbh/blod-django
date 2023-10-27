from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail


from .models import *
from .forms import *

def home(request):
    return render(request, 'home.html')

@login_required
def get_all_blogs(request):
    page = request.GET.get('page', 1)
    per_page = 5

    # If the user is not an admin, show only published blog posts
    if not request.user.is_superuser:
        blog_posts = BlogPost.objects.filter(is_published=True).order_by('-id')
    else:
        blog_posts = BlogPost.objects.all().order_by('-id')
    
    paginator = Paginator(blog_posts, per_page)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)

    return render(request, 'blog_list.html', {'blog_posts': blog_posts})

@login_required
def get_admins_blogs(request):
    if request.user.is_superuser:
        blog_posts = BlogPost.objects.all().order_by('-id')
    else:
        blog_posts = []
    
    return render(request, 'admin_blog_list.html', {'blog_posts': blog_posts, 'admin': request.user.is_superuser, 'logged_in': request.user.is_authenticated})


@login_required
def get_blog_details(request, post_id):
    try:
        post = BlogPost.objects.get(id=post_id)
        author = post.user
    except BlogPost.DoesNotExist:
        raise Http404("Blog post does not exist")

    blog_details = {
        'id': post.id,
        'title': post.title,
        'published_date': post.published_date.strftime("%Y-%m-%d"),
        'main_image': post.main_image.url if post.main_image else None,
        'content': post.content,
        'is_published': post.is_published,
        'author_name': author.username if author else ''
    }

    return render(request, 'blog_detail.html', {'blog_details': blog_details})

@login_required
def create_blog(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')  # Redirect unauthorized users to the login page

    funds = 0  # You need to set this variable based on your logic
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog_post = form.save(commit=False)
            new_blog_post.user = request.user
            new_blog_post.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('get_admins_blogs')
        else:
            messages.error(request, 'Form validation failed. Please check your inputs.')
    else:
        form = BlogPostForm()
    
    return render(request, 'create_blog.html', {'form': form, 'admin': request.user.is_superuser, 'logged_in': request.user.is_authenticated, 'funds': funds, 'username': request.user.username})



@login_required
def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    if request.user == post.user or request.user.is_superuser:
        post.delete()
        # Provide a success message if using Django messages framework
        return redirect('get_admins_blogs')
    else:
        # Handle permission denied or error
        return render(request, 'permission_denied.html')


@login_required
def edit_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)

    if request.user == post.user or request.user.is_superuser:
        if request.method == 'POST':
            form = EditBlogForm(request.POST,request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                # Provide a success message if using Django messages framework
                return redirect('get_admins_blogs')
            else:
                print('e>>>>>>>>>>>',form.errors)
        else:
            form = EditBlogForm(instance=post)

        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'edit_blog_post.html', context)
    else:
        # Handle permission denied or error
        return render(request, 'permission_denied.html')
    
@csrf_exempt
@login_required
def upload_image(request):
    if request.method == 'POST' and 'upload' in request.FILES:
        uploaded_file = request.FILES['upload']
        image_path = 'static/images/blogs/' + uploaded_file.name
        with open(image_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Return a JSON response with the image URL
        response_data = {
            'uploaded': 1,
            'fileName': uploaded_file.name,
            'url': '/' + image_path  # Adjust this path as needed
        }
    else:
        response_data = {'uploaded': 0, 'error': {'message': 'Failed to upload image'}}

    return JsonResponse(response_data)
    
    
def email_blog(request, post_id):
    if request.method == 'POST':
        form = EmailBlogForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(BlogPost, pk=post_id)
            sender_name = form.cleaned_data['sender_name']
            sender_email = form.cleaned_data['sender_email']
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_message = f"From: {sender_name} <{sender_email}>\n\n{message}"
            send_mail(subject, email_message, sender_email, [recipient_email])
            # Add a success message
            messages.success(request, 'Email sent successfully.')

            return redirect('get_blog_details', post_id=post.id)  # Redirect to the blog post page
    else:
        form = EmailBlogForm()

    return render(request, 'email_blog.html', {'form': form})    



@login_required
def add_comment(request, post_id):
    print('post_id>>>>>>>>>>',post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = BlogPost.objects.get(pk=post_id)
            comment.save()
            return redirect('get_blog_details', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form,'post_id':post_id})
