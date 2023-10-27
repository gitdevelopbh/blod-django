from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('get_all_blogs')  # Redirect to the blog's post list
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
