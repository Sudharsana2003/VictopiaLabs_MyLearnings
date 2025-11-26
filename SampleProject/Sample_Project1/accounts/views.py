from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        # Validation
        if not first_name or not last_name or not username or not email or not password1 or not password2:
            return render(request, "register.html", {"error": "All fields are required."})

        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already registered."})

        # Create the user
        User.objects.create_user(
            username=username,
            password=password1,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return render(request, "register.html", {"success": "Account created successfully!"})

    return render(request, "register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Django handles session
            return redirect("home")  # redirect to home page name
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")