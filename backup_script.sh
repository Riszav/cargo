
# === ПЕРЕМЕННЫЕ ===
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M')
DB_BACKUP_FILE="db_backup_$TIMESTAMP.dump"
cd ../var/www/bugin/
# === 1. СОЗДАЕМ БЭКАП БАЗЫ ===
echo "---------------------------------------"
echo "🔹 Делаем бэкап PostgreSQL... $TIMESTAMP"
docker exec -t cargo_postgres pg_dump -U cargo_user -d cargo_db -F c -f "$DB_BACKUP_FILE"
docker cp cargo_postgres:./"$DB_BACKUP_FILE" ./backups/

# === 2. ДОБАВЛЯЕМ В GIT ===
echo "🔹 Копируем бэкап в репозиторий..."
#docker cp bugin_postgres:"$DB_BACKUP_FILE" ./backups/
# ls ./backups/

# echo "🔹 Загружаем в Git..."
# git add .
# git commit -m "Автоматический бэкап $TIMESTAMP"
# git push

# echo "✅ Бэкап успешно загружен в Git!"
# echo "---------------------------------------"
echo "---------------------------------------"
echo "                 "
