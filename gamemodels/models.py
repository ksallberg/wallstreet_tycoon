from django.db                      import models

class Skill(models.Model):
   name  = models.CharField(max_length=100)
#   owner = models.ForeignKey(User,related_name='skill_owner_def')
   price = models.IntegerField()
   
   def __unicode__(self):
      return self.name

class Employee(models.Model):
   name   = models.CharField(max_length=100)
   skills = models.ManyToManyField(Skill)
   
   def __unicode__(self):
      return self.name