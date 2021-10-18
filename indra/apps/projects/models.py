from django.db import models
from apps.users.models import Company, Base
import os
# Create your models here.
class Project(Base):
    STATES = (
        ('AP', 'Approved'),
        ('RE', 'Reprobate'),
        ('AC', 'Accepted'),
        ('IR', 'In review'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='company')
    name = models.CharField("project name", max_length=250)
    details = models.CharField("project details", max_length=250, null=True, blank=True)
    file_1 = models.FileField(upload_to='documents/%Y/%m/%d', null=True, blank=True)
    state = models.CharField(max_length=2, default='AP', choices=STATES)
    def __str__(self):
        return str(self.company.name)

    def filename_1(self):
        return os.path.basename(self.file_1.name)