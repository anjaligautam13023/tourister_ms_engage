import json
from logging.handlers import RotatingFileHandler
from django.db import models
from pandas import DataFrame

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45,)
    email=models.CharField(max_length=45,)
    password=models.CharField(max_length=45,)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=45,)
    name = models.CharField(max_length=45,)
    user_id = models.IntegerField()
    clicks= models.IntegerField()
    rate= models.IntegerField()

    def activity_dataframe(self) -> DataFrame:
        return DataFrame.from_records(Activity.objects.all().values())

    
       

# Create your models here.
