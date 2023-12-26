from django.db import models
from django.contrib.auth.models import User



    

class Personal(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
       
   
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    other_name = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True)
    ghana_card_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField( default='default.jpeg', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    
    def __str__(self):
        return self.first_name
    
class Work(models.Model):  
    TEACHING_STAFF = 'Teaching staff'
    NON_TEACHING_STAFF = 'Non teaching staff'
    STAFF_CATEGORY_CHOICES = [
        (TEACHING_STAFF, 'Teaching staff'),
        (NON_TEACHING_STAFF, 'Non teaching staff'),
    ]
    
    DIRECTOR = 'Director'
    HUMAN_RESOURCE_MANAGEMENT_DEVELOPMENT= 'Human Resource and Development'
    PLANNING_STATISTICS = 'Plannning and Statistics'
    FINANACE_ADMINISTRATION = 'Finance and Administration'
    TEACHING_LEARNING = 'Teaching and Learning'
    DEPARTMENT_CHOICES =[
        (DIRECTOR, 'Director' ),
        (HUMAN_RESOURCE_MANAGEMENT_DEVELOPMENT, 'Human Resource and Development' ),
        (PLANNING_STATISTICS, 'Plannning and Statistics'),
        (FINANACE_ADMINISTRATION, 'Finance and Administration' ),
        (TEACHING_LEARNING, 'Teaching and Learning')
    ]  
     
    date_of_appointment = models.DateField(null=True, blank=True, help_text="Enter your date of current appointment")
    date_at_current_station = models.DateField(null=True, blank=True, help_text="Enter your date of current station")
    ssnit = models.CharField(max_length=10, null=True, blank=True)
    ntc_license_number = models.CharField(max_length=10, null=True, blank=True)
    rank = models.CharField(max_length=10, null=True, blank=True)
    date_promoted_to_rank =  models.CharField(max_length=10, null=True, blank=True) 
    staff_category = models.CharField(max_length=20, choices=STAFF_CATEGORY_CHOICES)
    academics= models.CharField(max_length=10, null=True, blank=True) 
    professional = models.CharField(max_length=10, null=True, blank=True) 
    schedule = models.CharField(max_length=10, null=True, blank=True) 
    department_category = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    personal = models.ForeignKey(Personal, on_delete=models. CASCADE)    
    
    
    def __str__(self):
        return f" Work info of {self.personal.first_name} {self.personal.last_name}"

    
    
class Nominal(models.Model):
    name_of_bank = models.CharField(max_length=50, null=True, blank=True)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    auth_number = models.CharField(max_length=50, null=True, blank=True)
    salary_grade_type = models.CharField(max_length=50, null=True, blank=True)
    salary_grade_level = models.CharField(max_length=50, null=True, blank=True)
    grade_step = models.CharField(max_length=50, null=True, blank=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f" Nominal data of {self.personal.first_name} {self.personal.last_name}"
    
    


    

    
     



