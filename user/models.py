# user/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import uuid

# --- Complaint Model (Deduced from your views) ---
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    # --- Using the categories from your uploaded file ---
    CATEGORY_CHOICES = [
        ('water', 'Water Leakage'),
        ('road', 'Broken Road/Potholes'),
        ('garbage', 'Garbage Collection'),
        ('electricity', 'Electricity Issues'),
        ('sewage', 'Sewage Problems'),
        ('parks', 'Park Maintenance'),
        ('streetlights', 'Street Light Issues'),
        ('traffic', 'Traffic Problems'),
        ('other', 'Other'),
    ]

    report_id = models.CharField(max_length=100, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)
    # --- ADDED: Lat/Lng fields for the map ---
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # ---
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # --- Contractor Relationship ---
    assigned_to = models.ForeignKey(
        'Contractor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_complaints'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.report_id:
            # Generate a unique report ID, e.g., URB12345
            self.report_id = f"URB{str(uuid.uuid4().int)[:6]}"
        
        # Update assigned_at timestamp when a contractor is first assigned
        if self.assigned_to and not self.assigned_at:
            self.assigned_at = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.report_id

# --- Contractor Model (MODIFIED) ---
class Contractor(models.Model):
    # --- Using the specializations from your uploaded file ---
    SPECIALIZATION_CHOICES = [
        ('water', 'Water Leakage'),
        ('road', 'Broken Road/Potholes'),
        ('garbage', 'Garbage Collection'),
        ('electricity', 'Electricity Issues'),
        ('sewage', 'Sewage Problems'),
        ('parks', 'Park Maintenance'),
        ('streetlights', 'Street Light Issues'),
        ('traffic', 'Traffic Problems'),
        ('other', 'Other'),
    ]

    # --- Fields from your admin form ---
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    area_assigned = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # --- NEW: Login Fields ---
    email = models.EmailField(unique=True) # This was already in your file
    password = models.CharField(max_length=128) # <-- THIS IS THE MISSING FIELD

    def __str__(self):
        return self.name

    # --- NEW: Save method to hash password ---
    def save(self, *args, **kwargs):
        # Hash the password if it's not already hashed (e.g., pbkdf2_sha256$)
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # --- NEW: Method to check password ---
    def check_password(self, raw_password):
        # Helper method to check password
        return check_password(raw_password, self.password)

