#!/bin/bash

# === Настройки ===
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M')
TELEGRAM_BOT_TOKEN="7939568906:AAFfOzFoQ1q1MbxM5bj1IHcSclap7z8ektk"
TELEGRAM_CHAT_ID="-4780961554"
EMAIL="riszav.01@gmail.com"
LOG_FILE="./certbot_renew.log"
exec > >(tee -a "$LOG_FILE") 2>&1

DOMAINS=("moicargo.kg")

# === Функция отправки сообщений в Telegram ===
send_telegram_message() {
    MESSAGE="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${MESSAGE}" > /dev/null
}

echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
echo "---------------------------------------------------------------------------------------------------------------------------"
echo "==================$TIMESTAMP====================="
echo "==================================================="
echo "==================================================="
echo "=== Остановка контейнеров, использующих 80 порт ==="
send_telegram_message "START <MOICARGO> 💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚"
send_telegram_message "🔴 Останавливаю Nginx для обновления SSL..."
docker stop cargo_nginx
echo "                "
echo "=== Обновление сертификатов ==="
echo "                "
send_telegram_message "-----------------------------------------"
for DOMAIN in "${DOMAINS[@]}"; do
    send_telegram_message "🔄 Обновляю сертификат для $DOMAIN..."

    certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos -m $EMAIL >> $LOG_FILE 2>&1
    CERTBOT_EXIT_CODE=$?

    echo "▶ Обновляю сертификат для $DOMAIN"
    certbot certonly --standalone -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"
    if [ $? -eq 0 ]; then
        echo "✅ Сертификат обновлён: $DOMAIN"
        send_telegram_message "✅ SSL для $DOMAIN успешно обновлён!"
    else
        echo "❌ Ошибка обновления SSL: $DOMAIN"
        send_telegram_message "⚠️ Ошибка обновления SSL для $DOMAIN!"
    fi
    echo "                "
    send_telegram_message "-----------------------------------------"
done
echo "                "
echo "=== Запуск контейнеров обратно ==="
echo "                "
send_telegram_message "🚀 Запускаю Docker..."
docker start cargo_nginx >> $LOG_FILE 2>&1 || send_telegram_message "⚠️ Ошибка при запуске Docker!"


echo "                "
echo "=== Завершение ==="
send_telegram_message "🎉 Обновление SSL завершено! (даже если были ошибки)"
send_telegram_message "END 💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜"
send_telegram_message "..."
echo "                "
echo "                "
echo "                "
echo "                "
