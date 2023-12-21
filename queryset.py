# Example queries
# 1. Number of male and female staff
male_staff_count = Staff.objects.filter(gender__name='Male').count()
female_staff_count = Staff.objects.filter(gender__name='Female').count()

# 2. Teaching and Non-teaching staff
teaching_staff_count = Staff.objects.filter(is_teaching_staff=True).count()
non_teaching_staff_count = Staff.objects.filter(is_teaching_staff=False).count()

# 3. Total number of staff
total_staff_count = Staff.objects.count()

# 4. Number of departments
total_departments = Department.objects.count()

# 5. Number of staff under each department
department_staff_count = Department.objects.annotate(num_staff=models.Count('staffdepartmentmapping')).values('name', 'num_staff')
