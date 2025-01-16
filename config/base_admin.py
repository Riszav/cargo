from django.utils.html import mark_safe
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
import inspect


class BaseImageAdmin(admin.ModelAdmin):
    @admin.display(description='предпросмотр')
    def view_image(self, obj, field_name, width=200):
        """
        Универсальный метод для генерации HTML предпросмотра изображений.
        
        :param obj: Объект модели
        :param field_name: Имя поля с изображением
        :param width: Ширина изображения
        :return: HTML-разметка изображения или "-"
        """
        image_field = getattr(obj, field_name, None)
        if image_field:
            return mark_safe(f"<img src='{image_field.url if hasattr(image_field, 'url') else image_field}' width={width} style='border-radius: 5px;'>")
        return "-"
    
    # @admin.display(description='предпросмотр')
    # def view_def_image_500(self, obj):
    #     data = inspect.currentframe().f_code.co_name.split('_')
    #     print(data)
    #     return self.view_image(obj, data[2], width=data[3])
    
    '''////////////// VIEW LOGO ///////////////'''
    @admin.display(description='предпросмотр логотипа')
    def view_product_logo(self, obj):
        return self.view_image(obj, 'product_logo', width=200)
    
    '''////////////// VIEW FOOTER LOGO ///////////////'''
    @admin.display(description='предпросмотр логотипа (footer)')
    def view_footer_logo(self, obj):
        return self.view_image(obj, 'footer_logo', width=200)

    '''////////////// VIEW LOGO ///////////////'''
    @admin.display(description='предпросмотр логотипа')
    def view_logo(self, obj):
        return self.view_image(obj, 'logo', width=200)

    '''////////////// VIEW FAVICON ///////////////'''
    @admin.display(description='предпросмотр фавикона')
    def view_favicon(self, obj):
        return self.view_image(obj, 'favicon', width=100)

    '''////////////// VIEW ICON ///////////////'''
    @admin.display(description='предпросмотр иконки')
    def view_icon(self, obj):
        return self.view_image(obj, 'icon', width=50)

    '''////////////// VIEW IMAGE ///////////////'''
    @admin.display(description='предпросмотр изображения')
    def view_mini(self, obj):
        return self.view_image(obj, 'image', width=100)
    
    @admin.display(description='предпросмотр изображения')
    def view_min(self, obj):
        return self.view_image(obj, 'image', width=200)

    @admin.display(description='предпросмотр изображения')
    def view_max(self, obj):
        return self.view_image(obj, 'image', width=400)
    
    '''////////////// VIEW IMAGE 1 ///////////////'''
    @admin.display(description='предпросмотр изображения')
    def view_min1(self, obj):
        return self.view_image(obj, 'image1', width=200)

    @admin.display(description='предпросмотр изображения')
    def view_max1(self, obj):
        return self.view_image(obj, 'image1', width=400)
        
    '''////////////// VIEW IMAGE 2 ///////////////'''
    @admin.display(description='предпросмотр изображения')
    def view_min2(self, obj):
        return self.view_image(obj, 'image2', width=200)

    @admin.display(description='предпросмотр изображения')
    def view_max2(self, obj):
        return self.view_image(obj, 'image2', width=400)

    '''////////////// VIEW BACKGROUND IMAGE ///////////////'''
    @admin.display(description='предпросмотр фона')
    def view_background_image(self, obj):
        return self.view_image(obj, 'background_image', width=400)



class BaseImageInline:
    @admin.display(description='предпросмотр')
    def view_image(self, obj, field_name, width=200):
        """
        Универсальный метод для генерации HTML предпросмотра изображений.
        
        :param obj: Объект модели
        :param field_name: Имя поля с изображением
        :param width: Ширина изображения
        :return: HTML-разметка изображения или "-"
        """
        image_field = getattr(obj, field_name, None)
        if image_field:
            return mark_safe(f"<img src='{image_field.url if hasattr(image_field, 'url') else image_field}' width={width} style='border-radius: 5px;'>")
        return "-"

    '''////////////// VIEW ICON ///////////////'''
    @admin.display(description='предпросмотр иконки')
    def view_icon(self, obj):
        return self.view_image(obj, 'icon', width=50)

    '''////////////// VIEW IMAGE ///////////////'''
    @admin.display(description='предпросмотр изображения')
    def view_min(self, obj):
        return self.view_image(obj, 'image', width=200)

    @admin.display(description='предпросмотр изображения')
    def view_max(self, obj):
        return self.view_image(obj, 'image', width=400)


class BaseVideoAdmin:

    @admin.display(description='предпросмотр')
    def view_video(self, obj):
        if obj.embed:  # Используем embed вместо video
            return mark_safe(f"""
                   <iframe width="400" height="250" style='border-radius: 5px;' 
                           src='{obj.embed}' frameborder="0" allowfullscreen>
                   </iframe>
               """)
        return "-"


class BaseSoloAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Возвращаем False, если объект уже существует
        return not self.model.objects.exists()

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Убираем кнопку "Сохранить и добавить другой объект"
        extra_context['show_save_and_add_another'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            # Если объект существует, переходим к его изменению
            return self.change_view(request, object_id=str(obj.pk))
        else:
            # Если объекта нет, перенаправляем на создание нового
            return HttpResponseRedirect(reverse(self.get_admin_url_name('add')))

    def get_admin_url_name(self, action):
        # Создает имя URL на основе текущей модели и действия
        return f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_{action}'
