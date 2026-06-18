from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Project, Bid, Profile
from .forms import ProjectForm, BidForm, SignupForm

# 1. Home Dashboard View
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'projects': projects})

# 2. Signup View with Live Error Catching
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('signup')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

# 3. Login View
def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = authenticate(request, username=u_name, password=p_word)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
    return render(request, 'core/login.html')

# 4. Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# 5. Create Project View
@login_required
def create_project(request):
    if request.user.profile.role != 'client':
        raise PermissionDenied
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'core/create_project.html', {'form': form})

# 6. Project Detail View
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bids = project.bids.all().order_by('-created_at')
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.project = project
            bid.freelancer = request.user
            bid.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = BidForm()
    return render(request, 'core/project_detail.html', {'project': project, 'bids': bids, 'form': form})

# 7. Update Bid Status View
@login_required
def update_bid_status(request, bid_id, action):
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.project.client == request.user:
        if action == 'accept':
            bid.status = 'Accepted'
            bid.save()
            bid.project.bids.exclude(id=bid.id).update(status='Rejected')
        elif action == 'reject':
            bid.status = 'Rejected'
            bid.save()
    return redirect('project_detail', pk=bid.project.pk)

# 8. My Bids View
@login_required
def my_bids(request):
    bids = Bid.objects.filter(freelancer=request.user)
    return render(request, 'core/my_bids.html', {'bids': bids})

# 9. My Projects View
@login_required
def my_projects(request):
    projects = Project.objects.filter(client=request.user)
    return render(request, 'core/my_projects.html', {'projects': projects})
from django.shortcuts import render
from .models import Project  # Agar Project model use ho raha hai

def home(request):
    # Aapke saare projects database se fetch karke home template par bhejega
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'projects': projects})