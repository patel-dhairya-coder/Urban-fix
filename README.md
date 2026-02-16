# UrbanFix: Smart Civic Issue Reporting & Management System
UrbanFix is a web-based platform designed to bridge the gap between citizens and local authorities. It allows residents to report civic issues (like potholes, broken streetlights, or waste management) directly to the administration, ensuring transparency and faster resolution through a streamlined digital workflow.

# 📋 Features
For Citizens
User Registration & Login: Secure authentication system for residents.

Complaint Submission: Easy-to-use form to report issues with image upload support for visual proof.

Unique Complaint ID: Every report gets a unique tracking ID automatically upon submission.

Status Tracking: Real-time updates on whether a complaint is Pending, In Progress, or Resolved.

For Administrators
Admin Dashboard: Comprehensive overview of all reported issues.

Work Assignment: Ability to assign specific complaints to registered Contractors.

Analytics Dashboard: Visual representation of data including total complaints, user growth, and resolution rates using charts.

For Contractors
Task Management: A dedicated panel to view assigned complaints.

Status Updates: Ability to update the progress of the work until the issue is marked as Resolved.

👥 User Roles
Citizen: Reports issues, uploads evidence, and tracks progress.

Admin: Oversees the system, manages users, and delegates tasks to contractors.

Contractor: The field worker/department responsible for fixing the reported issue and updating the status.

# 🛠 Tech Stack
Backend: Python, Django Framework

Frontend: HTML5, CSS3, JavaScript (Bootstrap for styling)

Database: SQLite (Default Django DB)

Imaging: Pillow (for image handling)

# 🚀 Installation Steps
Follow these steps to get the project running locally:

Clone the repository:

Bash
git clone https://github.com/your-username/UrbanFix.git
cd UrbanFix
Create a Virtual Environment:

Bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
Install Requirements:

Bash
pip install -r requirements.txt
Run Migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Start the Server:

Bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

# 📖 Usage Guide
Register as a Citizen to submit your first complaint.

Use the Django Admin (/admin) to create Contractor accounts.

Log in as Admin to view the Analytics and assign complaints to the created Contractors.

Log in as a Contractor to change the status of a complaint from "Pending" to "In Progress".

# 📂 Folder Structure
Plaintext
UrbanFix/
├── Urbanfix/      # Project settings and configuration
├── user/
├── admin_dashboard/ 
├── contractor/         
├── media/                 # Uploaded complaint images
├── static/                
├── templates/             
├── manage.py
├── .gitignore
├── requirements.txt
└── db.sqlite3

# 🔮 Future Enhancements
GPS Integration: Automatically fetch the user's location when reporting an issue.

Email Notifications: Notify citizens via email when their complaint status changes.

SMS Gateway: Send OTPs and alerts to users.

AI Categorization: Automatically categorize the type of issue based on the uploaded image.
