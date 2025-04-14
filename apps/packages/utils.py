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
            else:
                self.client.tarif_usa = 'Новичок'
        elif warehouse == 'Китай':
            self.client.tarif_china_weight = total_weight
            if total_weight >= VIP_THRESHOLD:
                self.client.tarif_china = 'VIP'
            else:
                self.client.tarif_china = 'Новичок'

    self.client.save()
    
def send_message(self, old_status):
    if self.status == 'На складе' and old_status != 'На складе':
        send_mail(
            subject=f'Ваша посылка: "{self.tracking_number}" На складе в {self.warehouse}',
            message=f'Уважаемый(ая), {self.client.first_name} {self.client.last_name}\n\n'
                    f'Статус Вашей посылки «Ждем на склад» был изменен на «На складе» в {self.warehouse}\n\n'
                    f'Номер заказа "{self.id}" , трек-номер заказа\n'
                    f'"{self.tracking_number}"\n'
                    f'Посылка будет отправлена в Бишкек в ближайшее время согласно расписанию.\n\n'
                    f'С Уважением, Moi Cargo.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.client.email]
        )
    elif self.status == 'Отправлена' and old_status != 'Отправлена':
        send_mail(
            subject=f'Ваша посылка: "{self.tracking_number}" Отправлена из {self.warehouse}',
            message=f'Уважаемый(ая), {self.client.first_name} {self.client.last_name}\n\n'
                    f'Статус Вашей посылки «На складе в {self.warehouse}» был изменен на «Отправлена из {self.warehouse}».\n\n'
                    f'Трек-номер заказа "{self.tracking_number}"\n\n'
                    f'Как только Ваша посылка будет в Бишкеке, мы уведомим вас по электронной почте.\n\n'
                    f'С Уважением, Moi Cargo.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.client.email]
        )
    elif self.status == 'Прибыла' and old_status != 'Прибыла':
        send_mail(
            subject=f'Ваша посылка: "{self.tracking_number}" Прибыла в Бишкек из {self.warehouse}',
            message=f'Уважаемый(ая), {self.client.first_name} {self.client.last_name}\n\n'
                    f'Статус Вашей посылки был изменен на «Прибыла в Бишкек из {self.warehouse}»\n\n'
                    f'Трек-номер заказа "{self.tracking_number}"\n\n'
                    f'Забрать посылку можно в нашем офисе по адресу: Киевская 107, ориентир ТЦ CARAVAN.\n\n'
                    f'С Уважением, Moi Cargo.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.client.email]
        )
    else:
        pass    
    
    # if self.status == 'Прибыла' and old_status != 'Прибыла':
    #     send_mail(
    #         subject=f'Ваша посылка: "{self.tracking_number}" Прибыла в Бишкек из "{self.warehouse}"',
    #         message=f'Уважаемый(ая), {self.client.first_name} {self.client.last_name}\n\n'
    #                 f'Статус Вашей посылки был изменен на Прибыла в Бишкек из “{self.warehouse}”.\n\n'
    #                 f'Номер заказа "{self.id}", трек-номер заказа "{self.tracking_number}"\n\n'
    #                 f'Вес посылки: {self.final_weight} кг. , стоимость доставки составляет: {self.delivery_cost} USD\n\n'
    #                 f'Комментарий: {self.system_comment}\n\n'
    #                 f'Забрать посылку можно в нашем офисе по адресу: ул. Киевская 107 1-этаж ориентир ТЦ Караван.\n\n\n\n'
    #                 f'С Уважением,\n'
    #                 f'MOI CARGO',
    #         from_email=DEFAULT_FROM_EMAIL,
    #         recipient_list=[self.client.email]
    #     )
    # elif self.status == 'Отправлена' and old_status != 'Отправлена':
    #     send_mail(
    #         subject=f'Ваша посылка: "{self.tracking_number}" Отправлена из  "{self.warehouse}"',
    #         message=f'Уважаемый(ая), {self.client.first_name} {self.client.last_name}\n\n'
    #                 f'Статус Вашей посылки "На складе в {self.warehouse}" был изменен на Отправлена из "{self.warehouse}".\n\n'
    #                 f'Номер заказа "{self.id}", трек-номер заказа "{self.tracking_number}"\n\n'
    #                 f'Как только Ваша посылка будет в Бишкек, мы уведомим вас по электронной почте.\n\n\n\n'
    #                 f'С Уважением,\n'
    #                 f'MOI CARGO',
    #         from_email=DEFAULT_FROM_EMAIL,
    #         recipient_list=[self.client.email]
    #     )
    # else:
    #     pass


def send_package_to_home(self):
    send_mail(
        subject=f'Заявка на отправку посылки на дом [Посылка: {self.tracking_number}]',
        message=f'Клиент: {self.client.first_name} {self.client.last_name}\n\n'
                f'Номер заказа "{self.id}", трек-номер заказа "{self.tracking_number}"\n\n'
                f'Ссылка на посылку: https://moicargo.kg/dashboard/edit-parcel/{self.id}\n\n',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=['riszav.01@gmail.com']
    )
