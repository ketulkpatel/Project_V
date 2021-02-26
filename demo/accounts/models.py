from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    contact=   models.IntegerField(max_length=10)
    email_id= models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    visit_type=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    date_from= models.DateField()
    date_to= models.DateField()
    user_id=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    is_Active=models.BooleanField(default=False)
    def __str__(self):
        return self.visit_type