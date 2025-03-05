from django.core.mail import send_mail
from config.settings.email_data import DEFAULT_FROM_EMAIL

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
    if self.status == 'Прибыла':
        send_mail(
            f'Ваша посылка: "{self.tracking_number}" Прибыла в Бишкек из "{self.warehouse}"',
            f'Посылка {self.id} прибыла на склад',
            DEFAULT_FROM_EMAIL,
            [self.client.email]
        )
    elif self.status == 'Отправлена':
        send_mail(
            f'Ваша посылка: "{self.tracking_number}" Отправлена из  "{self.warehouse}"',
            f'Посылка {self.id} отправлена',
            DEFAULT_FROM_EMAIL,
            [self.client.email]
        )
    else:
        pass


    