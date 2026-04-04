from decouple import config

ALLOWED_HOSTS = [config("DOMAIN_NAME", default=''), config('IP_ADDRESS')]

# Настройки базы данных для продакшена
DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE"),
        "NAME": config("SQL_DATABASE"),
        "USER": config("SQL_USER"),
        "PASSWORD": config("SQL_PASSWORD"),
        "HOST": config("SQL_HOST"),
        "PORT": config("SQL_PORT", cast=int),
    }
}

CSRF_TRUSTED_ORIGINS = [
    "http://"+config('IP_ADDRESS'), 
    "http://"+config('IP_ADDRESS')+":80", 
    "http://"+config('DOMAIN_NAME', default=''), 
    "https://"+config('DOMAIN_NAME', default=''), 
    "https://"+config('DOMAIN_NAME', default='')+":80", 
    ]

