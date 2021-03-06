from django.http import HttpResponse
from django.views import generic
from django.views.generic.list import ListView
from .models import SuperidToLoanLiability
from .models import EntityToPartnerType
from django.http import JsonResponse
from django.core import serializers
import json

#from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

class IndexView( generic.ListView):
    template_name = 'cdradmin/index.html'
    
    model= SuperidToLoanLiability
    
    def get_queryset(self):
        """Return the superid by order alphabetic."""
        return SuperidToLoanLiability.objects.order_by('superid')
   
    def get(self, *args, **kwargs):
    
        asjson = self.request.GET.get('asjson', "false")
        asjson=asjson.lower()=="true"
          
        if not asjson:
            return super(IndexView, self).get(*args, **kwargs)
             
        #https://stackoverflow.com/questions/41116841/object-is-not-json-serializable-django
        #to get the id of foreignkey
        #data = SuperidToLoanLiability.objects.all().values('superid', 'loan', 'liability')
        #data = SuperidToLoanLiability.objects.all()[0]
        json_obj = [
          {
            "superid": x.superid.superid,
            "account": x.superid.account,
            "ledger": x.ledger.ledger if x.ledger is not None else None,
            "subledger": x.subledger,
            "currency": x.currency_liability.name if x.currency_liability is not None else None,

            "liability_type": x.liability_type.short_description,

            "loan_type": x.loan_type.short_description,
            "loan_amount": x.loan_amount,
            "remaining_period":  x.get_remaining_period(),
            "country_of_utilization": x.country_of_utilization.cdr_code,


          } for x in SuperidToLoanLiability.objects.all()
        ]
        return JsonResponse(json_obj ,safe=False)



class EntityListView(ListView):

    template_name='cdradmin/entity_partnertype.html'
    #context_object_name = 'entity_partner_type'
    model = EntityToPartnerType
    

      
    def get_queryset(self):
        """Return the entity by order asc."""
        return EntityToPartnerType.objects.order_by('entity')
       
    def get(self, *args, **kwargs):   
         asjson = self.request.GET.get('asjson', "false")
         asjson=asjson.lower()=="true"

         if not asjson:
            return super(EntityListView, self).get(*args, **kwargs)


         json_obj = [
           {
            "entity": y.entity.entity_id,
            "partner_type": y.partner_type.name
            
          
            } for y in EntityToPartnerType.objects.all()
         ]

  

         #data = [{"entity": y.entity.entity_id, "partner_type":y.partner_type.name} for y in EntityToPartnerType.objects.all()]


         #json_json=serializers.serialize('json',json_obj,fields=('entity','partner_type'))
         #return HttpResponse(json_json, content_type="application/json")
         return JsonResponse(json_obj, safe=False)
    


        
         
                              

