from django.db import models

# Create your models here.
class User(models.Model):
    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    First = models.CharField(max_length=64)
    Last = models.CharField(max_length=64)
    Email = models.CharField(max_length=128, unique=True)
    Phone = models.IntegerField(unique=True) 
    boolChoice = (
        ("M","Male"),("F","Female")
        )
    Gender = models.CharField(max_length = 1,choices=boolChoice)

    def __str__(self):
        return f"{self.id} {self.First} {self.Last} {self.Email} {self.Phone} {self.Gender}"

class Village(models.Model):
    Name = models.CharField(max_length=64)
    Latitude = models.FloatField()
    Longitude = models.FloatField()

    def __str__(self):
        return f"{self.id} {self.Name} {self.Latitude} {self.Longitude}"


class Farmer(models.Model):
    Land_size = models.FloatField()
    Wheat_variety = models.CharField(max_length=20)
    Fertilizer_type = models.CharField(max_length=30)
    Fertilizer_amount = models.FloatField()
    Topography = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.id} {self.Land_size} {self.Wheat_variety} {self.Fertilizer_type} {self.Fertilizer_amount} {self.Topography}"

class AnalyzedData(models.Model):
    SowingDate = models.CharField(max_length=20)
    HarvestingDate = models.CharField(max_length=20)
    pesticideRecommendation = models.CharField(max_length=30)
    DataPublished = models.DateField()

    def __str__(self):
        return f"{self.id} {self.SowingDate} {self.HarvestingDate} {self.pesticideRecommendation} {self.DataPublished}"
