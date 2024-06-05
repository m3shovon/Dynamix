from django.db import models

class PersonalInfo(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True) 
    profile_pic = models.ImageField(upload_to='resume_pics', blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    github = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=20, null=True, blank=True)
    marrital_status = models.CharField(max_length=20, null=True, blank=True)

class About(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE) 
    description1 = models.TextField(null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)

class Education(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE) 
    field_of_study = models.CharField(max_length=20, null=True, blank=True)
    school = models.CharField(max_length=20, null=True, blank=True)
    degree = models.CharField(max_length=20, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

class Skill(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)

class WorkExperience(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE) 
    title = models.CharField(max_length=20, null=True, blank=True)
    employee_type = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=20, null=True, blank=True)
    work_type = models.CharField(max_length=20, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)

class Interest(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE) 
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Certification(models.Model):
    personal = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
