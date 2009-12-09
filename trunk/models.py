from django.db import models
from django_freshbooks import api
from django_freshbooks.settings import *
from datetime import date

STATUS_CHOICES = (
                 ('sent','sent'),
                 ('viewed','viewed'),
                 ('paid','paid'),
                 ('draft','draft'),
                 )
FREQ_CHOICES = (
                 ('weekly','weekly'),
                 ('2 weeks','2 weeks'),
                 ('4 weeks','4 weeks'),
                 ('monthly','monthly'),
                 ('3 months','3 months'),
                 ('6 months','6 months'),
                 ('yearly','yearly'),
                 ('2 years','2 years'),
                 )

class Line(api.BaseObject):
    TYPE_MAPPINGS = {'invoice_id' : 'int', 'client_id' : 'int',
        'po_number' : 'int', 'discount' : 'float', 'amount' : 'float',
        'date' : 'datetime', 'amount_outstanding' : 'float', 
        'paid' : 'float'}
    
    name = models.CharField(max_length=255,blank=True)
    description = models.CharField(max_length=255,blank=True)
    unit_cost = models.DecimalField(max_digits=2,decimal_places=2,blank=True)
    quantity = models.IntegerField(blank=True)
    tax1_name = models.CharField(max_length=255,blank=True)
    tax2_name = models.CharField(max_length=255,blank=True)
    tax1_percent = models.DecimalField(max_digits=2,decimal_places=2,blank=True)
    tax2_percent = models.DecimalField(max_digits=2,decimal_places=2,blank=True)
   
    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("line.create", {None:self})


class Category(api.BaseObject):
    object_name = 'category'
    name = models.CharField(max_length=255)
    
    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("category.create", {None:self}) 
            
class Task(api.BaseObject):
    object_name = 'task'
    TYPE_MAPPINGS = {'rate': 'float', }
    
    name = models.CharField(max_length=255)
    billable = models.BooleanField()
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.CharField(max_length=255)
    
    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("task.create", {None:self}) 
            
            
class Payment(api.BaseObject):
    object_name = 'payment'
    TYPE_MAPPINGS = {'client_id': 'int', 'invoice_id': 'int'}
    
    client_id = models.IntegerField()
    invoice_id = models.IntegerField()
    date = models.DateField()
    amount = models.DeciamlField(max_digits=10,decimal_places=2)
    type = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)
    
    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("payment.create", {None:self})
        
class Recurring(api.BaseObject):
    object_name = 'recurring'
    TYPE_MAPPINGS = {'recurring_id' : 'int', 'client_id' : 'int',
        'po_number' : 'int', 'discount' : 'float', 'amount' : 'float',
        'date' : 'datetime', 'amount_outstanding' : 'float', 
        'paid' : 'float'}
    client_id = models.IntegerField()
    date = models.DateField(default=date.today(),blank=True)
    po_number = models.CharField(max_length=255,blank=True)
    discount = models.DecimalField(blank=True,max_digits=2,decimal_places=2)
    occurrences = models.IntegerField(help_text='0 = infinite',default=1)
    frequency = models.CharField(max_length=50, choices=FREQ_CHOICES)
    send_email = models.BooleanField()
    send_snail_mail = models.BooleanField()
    notes = models.CharField(max_length=255,blank=True,)
    terms = models.CharField(max_length=255,blank=True)
    return_uri = models.CharField(max_length=255,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    p_street1 = models.CharField(max_length=255,blank=True)
    p_street2 = models.CharField(max_length=255,blank=True)
    p_city = models.CharField(max_length=255,blank=True)
    p_state = models.CharField(max_length=255,blank=True)
    p_country = models.CharField(max_length=255,blank=True)
    p_code = models.CharField(max_length=255,blank=True)

    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("invoice.create", {None:self})
        
class Invoice(api.BaseObject):
    object_name = 'invoice'
    TYPE_MAPPINGS = {'invoice_id' : 'int', 'client_id' : 'int',
        'po_number' : 'int', 'discount' : 'float', 'amount' : 'float',
        'date' : 'datetime', 'amount_outstanding' : 'float', 
        'paid' : 'float'}
    client_id = models.IntegerField()
    number = models.CharField(max_length=255,blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='draft')
    date = models.DateField(default=date.today(),blank=True)
    po_number = models.CharField(max_length=255,blank=True)
    discount = models.DecimalField(blank=True,max_digits=2,decimal_places=2)
    notes = models.CharField(max_length=255,blank=True,)
    terms = models.CharField(max_length=255,blank=True)
    return_uri = models.CharField(max_length=255,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    p_street1 = models.CharField(max_length=255,blank=True)
    p_street2 = models.CharField(max_length=255,blank=True)
    p_city = models.CharField(max_length=255,blank=True)
    p_state = models.CharField(max_length=255,blank=True)
    p_country = models.CharField(max_length=255,blank=True)
    p_code = models.CharField(max_length=255,blank=True)

    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("invoice.create", {None:self})
        
    
        
class Client(api.BaseObject):
    TYPE_MAPPINGS = {'client_id' : 'int'}
    object_name = 'client'
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=10, blank=True)
    work_phone = models.CharField(max_length=20,blank=True)
    home_phone = models.CharField(max_length=20,blank=True)
    mobile = models.CharField(max_length=20,blank=True)
    fax = models.CharField(max_length=20,blank=True)
    notes = models.CharField(max_length=255,blank=True,)
    p_street1 = models.CharField(max_length=255,blank=True)
    p_street2 = models.CharField(max_length=255,blank=True)
    p_city = models.CharField(max_length=255,blank=True)
    p_state = models.CharField(max_length=255,blank=True)
    p_country = models.CharField(max_length=255,blank=True)
    p_code = models.CharField(max_length=255,blank=True)
    s_street1 = models.CharField(max_length=255,blank=True)
    s_street2 = models.CharField(max_length=255,blank=True)
    s_city = models.CharField(max_length=255,blank=True)
    s_state = models.CharField(max_length=255,blank=True)
    s_country = models.CharField(max_length=255,blank=True)
    s_code = models.CharField(max_length=255,blank=True)

    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("client.create", {None:self})


class Item(api.BaseObject):
    object_name = 'item'
    TYPE_MAPPINGS = {'item_id' : 'int', 'unit_cost' : 'float','quantity' : 'int', 'inventory' : 'int'}
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    unit_cost = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField()
    inventory = models.IntegerField(blank=True)
 
    def save(self):
        if not self.id:
            api.setup(FRESHBOOKS_URL,FRESHBOOKS_TOKEN);
            response = api.call_api("item.create", {None:self})

