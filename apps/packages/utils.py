

def update_tarif(self):
    from django.db.models import Sum
    from apps.packages.models import Package
    
    warehouse_weights = (
        Package.objects
        .filter(client=self.client)
        .values('warehouse')
        .annotate(total_weight=Sum('final_weight'))
    )
    # print(warehouse_weights)

    VIP_THRESHOLD = 50

    for entry in warehouse_weights:
        warehouse = entry['warehouse']
        total_weight = entry['total_weight']
        print(warehouse)
        print(total_weight)
        
        if warehouse == 'США':
            self.client.tarif_usa_weight = total_weight
            if total_weight >= VIP_THRESHOLD:
                self.client.tarif_usa = 'VIP'
        elif warehouse == 'Турция':
            self.client.tarif_turkey_weight = total_weight
            if total_weight >= VIP_THRESHOLD:
                self.client.tarif_turkey = 'VIP'
        elif warehouse == 'Китай':
            self.client.tarif_china_weight = total_weight
            if total_weight >= VIP_THRESHOLD:
                self.client.tarif_china = 'VIP'
        elif warehouse == 'Япония':
            self.client.tarif_japan_weight = total_weight
            if total_weight >= VIP_THRESHOLD:
                self.client.tarif_japan = 'VIP'

    self.client.save()
    
    
def send_message(self):
    pass
    