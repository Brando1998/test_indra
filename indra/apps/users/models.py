from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.BooleanField("status", default=True)
        
    class Meta:
        abstract = True

class Company(Base):
    name=models.CharField("name", max_length=250)
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        
    def __str__(self):
        return str(self.name)

class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='company')
    mobile_number = models.CharField("mobile number", max_length=250, null=True, blank=True)
    file_1 = models.FileField(upload_to='documents/%Y/%m/%d', null=True, blank=True)
    file_2 =  models.FileField(upload_to='documents/%Y/%m/%d', null=True, blank=True)
    def __str__(self):
        return str(self.company.name)

    def filename_1(self):
        return os.path.basename(self.file_1.name)
    
    def filename_2(self):
        return os.path.basename(self.file_2.name)