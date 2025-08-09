echo '.............................'
echo 'Begin Restart'

cd /root/cargo
git pull
docker-compose down
docker-compose up --build -d

echo 'FINISH'
