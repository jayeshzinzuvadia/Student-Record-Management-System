from django.db import models

# Create your models here.

class Student(models.Model):
    # Some predefined choices
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    CAREER_PREFERENCE_TYPES = (
        ('H', 'Higher Studies'),
        ('J', 'Job'),
    )
    # Student's personal information
    id_no = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=80)
    branch = models.CharField(max_length=2)
    admission_category = models.CharField(max_length=3)
    cast_category = models.CharField(max_length=5)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    dob = models.DateField()
    email_id = models.CharField(max_length=100)
    contact_no_1 = models.CharField(max_length=12)
    contact_no_2 = models.CharField(max_length=12)
    # Student's academic information
    ssc_result = models.DecimalField(max_digits=5, decimal_places=2)
    hsc_result = models.DecimalField(max_digits=5, decimal_places=2)
    diploma_result = models.DecimalField(max_digits=5, decimal_places=2)
    spi_sem_1 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_2 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_3 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_4 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_5 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_6 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_7 = models.DecimalField(max_digits=4, decimal_places=2)
    spi_sem_8 = models.DecimalField(max_digits=4, decimal_places=2)
    cpi = models.DecimalField(max_digits=4, decimal_places=2)
    # Student's address information
    address_1 = models.CharField(max_length=150)
    address_2 = models.CharField(max_length=150)
    address_3 = models.CharField(max_length=150)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pin_code = models.CharField(max_length=10)
    # Student's placement/internship data
    career_preference = models.CharField(max_length=1, choices=CAREER_PREFERENCE_TYPES)
    internship = models.CharField(max_length=100)
    placement = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    other_placement_1 = models.CharField(max_length=100)
    other_placement_2 = models.CharField(max_length=100)
    # Batch year
    batch_year = models.IntegerField()

class Skill(models.Model):
    sid = models.BigAutoField(primary_key=True)
    # Student's skill set information
    stu_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    skills = models.CharField(max_length=50)

class Achievements(models.Model):
    aid = models.BigAutoField(primary_key=True)
    # Student's achievements information
    stu_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    achievement_details = models.CharField(max_length=50)
