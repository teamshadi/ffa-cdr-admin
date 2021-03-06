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
     account = models.CharField(max_length=6)
     name = models.CharField(max_length=255)
  
     class Meta:
          unique_together = ("superid", "account")  
          ordering = ("superid", "account")

     def __str__(self):
        #return str(self.superid)+": "+self.name
        return "%s/%s: %s"%(self.superid, self.account, self.name) 


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
      #: numeric code in MF
      code = models.IntegerField(default=0)

      name = models.CharField(max_length=255)
      description = models.CharField(max_length=255)

     
#      class Meta:
 #        ordering = ('name',)

      def __str__(self):
           return " %s:%s"%(self.name, self.description)



class Country(models.Model):
     cdr_code = models.IntegerField(default=0, unique=True)
     name = models.CharField(max_length=255, unique=True)
     class Meta:
       ordering = ('name',)
     
     def __str__(self):
        return "%s (%s)"%(self.name, self.cdr_code)


class Ledger(models.Model):

     ledger = models.CharField(max_length=255)
     name = models.CharField(max_length=255)



     def __str__(self):
       
        return "%s: %s"%(self.ledger, self.name)
   


from django.core.exceptions import ValidationError 

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

import datetime as dt

class SuperidToLoanLiability(models.Model):
     
     superid = models.ForeignKey(Superid)

     loan_type = models.ForeignKey(Loan)
     loan_amount = models.IntegerField(default=0, verbose_name="Loan amount (use 0 for 'From MF')")
     liability_type = models.ForeignKey(Liability)

     #: Instead of setting "guarantee_..." fields which are now deprecated,
     #: just point a liability to another one as the guarantee for which it is
     guarantee_for = models.ForeignKey('SuperidToLoanLiability', blank=True, null=True, default=None)

     maturity_date = models.DateField(blank=True,null=True)

     #: Ledger can be NULL for TSR/TBI only
     ledger = models.ForeignKey(Ledger, blank=True, null=True, default=None, verbose_name="Ledger (skip for TSR/TBI)")

     #: Single digit from 0 to 9
     subledger = models.IntegerField(default=0, validators = [MinValueValidator(0), MaxValueValidator(9)])

     country_of_utilization= models.ForeignKey(Country,blank=True, null=True)
     currency_liability = models.ForeignKey(Currency, related_name='currency_liability')

     closed = models.BooleanField(default=False)     
 
     comments = models.CharField(max_length=600, blank=True)


     def clean(self,*args, **kwargs):
       if self.liability_type.short_description in ['TSR','TBI']:
         if self.ledger is not None:
           raise ValidationError("Cannot set ledger for TSR/TBI")
       else:
         if self.ledger is None:
           raise ValidationError("Ledger is required for all liability types *other* than TSR/TBI")

       if self.guarantee_for is not None:
         if self.currency_liability != self.guarantee_for.currency_liability:
           raise ValidationError({"guarantee_for": "Liability currency is '%s', but currency of 'guarantee for' is '%s'. Please use the same currency for both, or convert one of them to the other one's currency."%(self.currency_liability.name, self.guarantee_for.currency_liability.name)})

       return super().clean(*args, **kwargs)

     class Meta:
        unique_together = (
          ('superid', 'ledger', 'subledger', 'currency_liability'),
        )
        ordering = ['superid__superid', 'ledger__ledger', 'subledger', 'currency_liability']

     def __str__(self):
         return "%s: %s, %s, %s, %s, %s"%(self.superid, self.display_ledger_text(), self.subledger, self.currency_liability, self.loan_type.short_description, self.liability_type.short_description)


     def save(self,*args, **kwargs):
       # use "iexact" below for case insensitive matching
       beirut, created = Country.objects.get_or_create(cdr_code=101, name__iexact='beirut')
       if self.country_of_utilization is None:
         self.country_of_utilization = beirut

       return super().save(*args, **kwargs)

     def display_ledger_title(self):
       if self.liability_type.short_description in ['TSR','TBI']:
         return "N/A since %s"%self.liability_type.short_description
       return self.ledger.name

     def display_ledger_text(self):
       if self.liability_type.short_description in ['TSR','TBI']:
         return "-"
       return self.ledger.ledger

     def get_remaining_period(self):
       if (self.maturity_date is None)  : return 0
       else:
           if not diff_month(self.maturity_date, dt.datetime.now())>0: return 0
       
       return diff_month(self.maturity_date, dt.datetime.now())
