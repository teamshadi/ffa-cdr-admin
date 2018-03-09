from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Loan(models.Model):


     short_description = models.CharField(max_length=255)
     long_description = models.CharField(max_length=600)


     def __str__(self):
        return "%s: %s" %(self.short_description, self.long_description)

class Liability(models.Model):
    
      short_description = models.CharField(max_length=255)
      long_description = models.CharField(max_length=600)

      def __str__(self):
        return "%s: %s" %(self.short_description, self.long_description)


class Superid(models.Model):
     
     superid = models.IntegerField(default=0)
     name = models.CharField(max_length=255)
   
     class Meta:
          unique_together = ("superid", "name")  
          


     def __str__(self):
        #return str(self.superid)+": "+self.name
        return "%s: %s"%(self.superid, self.name) 

class Partner_type(models.Model):
       code = models.IntegerField(default=0)
       name = models.CharField(max_length=255)

       def __str__(self):

           return "%s: %s"%(self.code, self.name)


class Entity(models.Model):
      entity_id = models.IntegerField(default=0)
      name = models.CharField(max_length=255) 
   
    
      def __str__(self):
     
          return "%s: %s"%(self.entity_id, self.name)

class EntityToPartnerType(models.Model):
      entity = models.ForeignKey(Entity)
      partner_type = models.ForeignKey(Partner_type)

      def __str__(self):

          return "%s: %s"%(self.entity, self.partner_type)

class Currency(models.Model):
      code = models.IntegerField(default=0)
      name = models.CharField(max_length=255)
      description = models.CharField(max_length=255)

     
#      class Meta:
 #        ordering = ('name',)

      def __str__(self):
           return " %s:%s"%(self.name, self.description)



class Country(models.Model):

     country = models.IntegerField(default=0)
     name = models.CharField(max_length=255)
     
   
     class Meta:
       ordering = ('name',)
     
     def __str__(self):
        
        return " %s"%(self.name)


class Ledger(models.Model):

     ledger = models.CharField(max_length=255)
     name = models.CharField(max_length=255)



     def __str__(self):
       
        return "%s: %s"%(self.ledger, self.name)
   


 
class SuperidToLoanLiability(models.Model):
     
     superid = models.ForeignKey(Superid)

     loan_type = models.ForeignKey(Loan)
     loan_amount = models.IntegerField(default=0)
     liability_type = models.ForeignKey(Liability)

     #: deprecated
     guarantee_amount = models.IntegerField(default=0)

     #: deprecated
     guarantee_type = models.CharField(max_length=255)

     #: Instead of setting "guarantee_..." fields which are now deprecated,
     #: just point a liability to another one as the guarantee for which it is
     guarantee_for = models.ForeignKey('SuperidToLoanLiability', null=True, default=None)

     maturity_date = models.DateField(blank=True,null=True)
     ledger = models.ForeignKey(Ledger)
     subledger = models.IntegerField(default=0, validators = [MinValueValidator(0), MaxValueValidator(9)])

     country_of_utilization= models.ForeignKey(Country,blank=True, null=True)
     currency_liability = models.ForeignKey(Currency,blank=True, null=True, related_name='currency_liability')
     #: deprecated
     guarantee_currency = models.ForeignKey(Currency,blank=True, null=True,related_name='guarantee_currency')

     closed = models.BooleanField(default=False)     
 
#     if closed == True:
 #     self.fields['guarantee'].required = False
  #    self.fields['maturity_date'].required= False
    #  self.fields['ledger'].required= False
     # self.fields['country_of_utilization'].required= False
   #   guarantee = forms.IntegerField(required=False, blank=True, null=True)    
     # ledger = forms.CharField(required=False, blank=True, null=True)
    #  country_of_utilization = forms.CharField(required=False, blank=True, null=True)
      
     class Meta:
        unique_together = (
          ('superid', 'ledger', 'subledger', 'currency_liability'),
        )
        ordering = ['superid__superid', 'ledger__ledger', 'subledger', 'currency_liability']

     def __str__(self):
       # return "%s: %s,%s,%s, %s,%s,%s, %s, %s"%(self.superid, self.loan_type, self.liability_type, self.guarantee_amount, self.maturity_date, self.country_of_utilization,self.ledger,self.closed)
         return "%s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(self.superid, self.loan_type,self.loan_amount, self.liability_type, self.guarantee_amount,self.guarantee_type,self.ledger, self.maturity_date,self.country_of_utilization,self.currency_liability,self.guarantee_currency,self.closed)


     def save(self,*args, **kwargs):
       lebanon = Country.objects.get(name__iexact='lebanon')
       if self.country_of_utilization is None:
         self.country_of_utilization = lebanon

       return super().save(*args, **kwargs)
