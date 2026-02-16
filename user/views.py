from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, ComplaintSerializer
from django.http import JsonResponse
from .models import Complaint

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for creating a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

# 2. API ViewSet for Complaints (Handles all CRUD operations)
class ComplaintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and create their own complaints.
    """
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access

    def get_queryset(self):
        """
        This view should return a list of all the complaints
        for the currently authenticated user.
        """
        return Complaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically associate the complaint with the logged-in user upon creation.
        """
        serializer.save(user=self.request.user)
        
def home(request):
    complaints = []
    status_counts = {
        'pending': 0,
        'in_progress': 0,
        'resolved': 0,
    }
    tracked_complaint = request.session.pop('tracked_complaint', None)
    if request.user.is_authenticated:
        complaints = Complaint.objects.filter(user=request.user)
        counts = complaints.values('status').annotate(total=Count('status'))
        for c in counts:
            status_counts[c['status']] = c['total']

    return render(request, "user/home.html", {
        'complaints': complaints,
        'status_counts': status_counts,
        'tracked_complaint': tracked_complaint,
    })

@login_required # Ensure only logged-in users can access this view
def report(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        photo = request.FILES.get('photo') 
        
        # --- GET THE COORDINATES FROM THE FORM ---
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # ------------------------------------------

        if not all([category, location, description, latitude, longitude]):
            messages.error(request, "Please fill in all required fields and select a location on the map.")
            return redirect('home') # Or render the form again with errors
        
        try:
            complaint = Complaint.objects.create(
                user=request.user,
                category=category,
                location=location,
                description=description,
                photo=photo,
                # --- SAVE THE COORDINATES TO THE DATABASE ---
                latitude=latitude,
                longitude=longitude
                # ---------------------------------------------
            )
            # The .save() is not needed when using .create()
            messages.success(request, f"Your complaint has been submitted successfully! Your Report ID is {complaint.report_id} ")
            return redirect('home') # Redirect to home or a success page
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('home')
            
    return render(request, "user/home.html")

def track_complaint(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        try:
            complaint = Complaint.objects.get(report_id=report_id)
            # Store the complaint in the session to be accessed by the home view
            request.session['tracked_complaint'] = {
                'report_id': complaint.report_id,
                'category': complaint.category,
                'location': complaint.location,
                'status': complaint.status,
                'submitted_at': complaint.submitted_at.strftime("%b %d, %Y"),
            }
            return redirect('home')
        except Complaint.DoesNotExist:
            messages.error(request, f"No complaint found with ID: {report_id}.")
            return redirect("home")
    return redirect("home")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! Please sign in.")
                return redirect('signin')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
    return render(request, "user/signup.html") # Assuming you'll create a signup.html

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:   # ✅ Correct condition
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')
    return render(request, "user/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def role_select(request):
    return render(request, 'user/role_select.html')