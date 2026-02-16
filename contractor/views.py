# contractor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.models import Contractor, Complaint
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from functools import wraps
from django.db import models # <-- NEW: Added this import

# --- Decorator for Contractor Login ---
def contractor_login_required(view_func):
# ... (rest of the file remains the same) ...
    """
    Decorator to ensure a contractor is logged in via session.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        contractor_id = request.session.get('contractor_id')
        if not contractor_id:
            messages.error(request, "Please log in to access this page.")
            return redirect('contractor:login')
        
        try:
            contractor = Contractor.objects.get(id=contractor_id, is_active=True)
            request.contractor = contractor # Attach contractor to request
        except Contractor.DoesNotExist:
            messages.error(request, "Your account is not active or does not exist.")
            # Clear the bad session key
            if 'contractor_id' in request.session:
                del request.session['contractor_id']
            return redirect('contractor:login')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- Contractor Login ---
def contractor_login(request):
# ... (rest of the file remains the same) ...
    if request.session.get('contractor_id'):
        return redirect('contractor:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, "contractor/login.html")

        try:
            contractor = Contractor.objects.get(email=email)
            if contractor.check_password(password) and contractor.is_active:
                request.session['contractor_id'] = contractor.id
                messages.success(request, f"Welcome, {contractor.name}!")
                return redirect('contractor:dashboard')
            else:
                messages.error(request, "Invalid credentials or account inactive.")
        except Contractor.DoesNotExist:
            messages.error(request, "Invalid credentials or account inactive.")
            
    return render(request, "contractor/login.html")

# --- Contractor Logout ---
@contractor_login_required
def contractor_logout(request):
# ... (rest of the file remains the same) ...
    if 'contractor_id' in request.session:
        del request.session['contractor_id']
    messages.success(request, "You have been logged out.")
    return redirect('contractor:login')

# --- Contractor Dashboard (Analytics) ---
@contractor_login_required
def dashboard(request):
# ... (rest of the file remains the same) ...
    contractor = request.contractor
    
    # Get all complaints assigned to this contractor
    complaints = Complaint.objects.filter(assigned_to=contractor)

    # --- KPIs ---
    total_assigned = complaints.count()
    total_pending = complaints.filter(status__in=['pending', 'in_progress']).count()
    total_resolved = complaints.filter(status='resolved').count()
    total_rejected = complaints.filter(status='rejected').count()

    # --- Pie Chart: Status Distribution ---
    status_distribution = complaints.values('status').annotate(total=Count('status')).order_by('status')
    pie_labels = [s['status'].replace('_', ' ').title() for s in status_distribution]
    pie_data = [s['total'] for s in status_distribution]

    # --- Bar Chart: Complaints Assigned per Month (Last 6 Months) ---
    today = timezone.now()
    six_months_ago = today - timedelta(days=180)
    
    monthly_data = complaints.filter(assigned_at__gte=six_months_ago) \
                             .annotate(month=models.functions.TruncMonth('assigned_at')) \
                             .values('month') \
                             .annotate(count=Count('report_id')) \
                             .order_by('month')

    bar_labels = [m['month'].strftime("%b %Y") for m in monthly_data]
    bar_data = [m['count'] for m in monthly_data]

    context = {
        'total_assigned': total_assigned,
        'total_pending': total_pending,
        'total_resolved': total_resolved,
        'total_rejected': total_rejected,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'contractor': contractor,
    }
    return render(request, "contractor/dashboard.html", context)

# --- Contractor Complaint List ---
@contractor_login_required
def complaint_list(request):
# ... (rest of the file remains the same) ...
    contractor = request.contractor
    
    # Get all complaints assigned to this contractor, newest first
    complaints = Complaint.objects.filter(assigned_to=contractor).select_related('user').order_by('-assigned_at')
    
    context = {
        'complaints': complaints,
        'contractor': contractor,
    }
    return render(request, "contractor/complaint_list.html", context)

# --- Contractor Complaint Detail (with Status Update) ---
@contractor_login_required
def complaint_detail(request, report_id):
# ... (rest of the file remains the same) ...
    contractor = request.contractor
    
    # Get the complaint, ensuring it is assigned to this contractor
    complaint = get_object_or_404(Complaint, report_id=report_id, assigned_to=contractor)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed_statuses = ['resolved', 'rejected'] # Contractors can only set these
        
        if new_status in allowed_statuses:
            complaint.status = new_status
            complaint.save()
            messages.success(request, f"Complaint {report_id} status updated to {complaint.get_status_display()}.")
            return redirect('contractor:complaint_list')
        else:
            messages.error(request, "Invalid status update.")

    context = {
        'complaint': complaint,
        'contractor': contractor,
        # Only allow setting to resolved or rejected
        'status_choices': [c for c in Complaint.STATUS_CHOICES if c[0] in ['resolved', 'rejected']],
    }
    return render(request, "contractor/complaint_detail.html", context)

def home(request):
    return render(request, "user/home.html")
