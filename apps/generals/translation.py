from modeltranslation.translator import register, TranslationOptions
from . import models
    

@register(models.Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(models.AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    

@register(models.AboutUsPage)
class AboutUsPageTranslationOptions(TranslationOptions):
    fields = ('text', )


@register(models.OurServices)
class OurServicesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    

@register(models.ApplicationSettings)
class ApplicationSettingsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(models.FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
    

@register(models.HowItWorks)
class HowItWorksTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(models.PriceAndPayment)
class PriceAndPaymentTranslationOptions(TranslationOptions):
    fields = ('type_of_service', 'price_usa', 'price_turkey', 'price_china_air', 'price_china_car', 'commission')
    
    
@register(models.PaymentData)
class PaymentDataTranslationOptions(TranslationOptions):
    fields = ('subtitle', 'description', 'description_weight', 'text_weight', 'description_payment')
    
    
@register(models.News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    
    
@register(models.PVZ)
class PVZTranslationOptions(TranslationOptions):
    fields = ('title', 'location','working_hours')
   
