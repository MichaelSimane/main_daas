# from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class DAAS_Manager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError("email is required. ")
        if not first_name:
            raise ValueError("First Name  is required. ")
        if not last_name:
            raise ValueError("Last Name  is required. ")
        # if not phone_number:
        #     raise ValueError("Phone Number is required. ")
      
        # if not passwordConf:
        #     raise ValueError("Password confirmation is required. ")
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        # user.is_admin = False
        # user.is_staff = False
        # user.is_active = True
        # user.is_superuser = False
        # user.set_password(password)
        # user.save(using=self._db)
        # return user
    def create_superuser(self,email, first_name,last_name, phone_number, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            password = password,
            # passwordConf = passwordConf 
           

        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class DAAS_User(AbstractBaseUser):
    
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name",max_length=100)
    phone_number = models.IntegerField(verbose_name="Phone Number", unique=True)
    email = models.EmailField(verbose_name="Email Address",max_length=200,  unique=True)
    date_joined = models.DateField(verbose_name="Date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # region = models.CharField(max_length=15)
    # if is_admin == False:
    #     USERNAME_FIELD = 'phone_number'
    #     REQUIRED_FIELDS = [   'first_name', 'last_name', 'password', 'email']
    # else:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [  'phone_number', 'first_name', 'last_name', 'password']
    objects = DAAS_Manager()

    def __str__(self):
        return self.first_name + " " + self.last_name
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True 
