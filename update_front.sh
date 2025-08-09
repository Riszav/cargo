echo '.............................'
echo 'Begin Restart'

cd /root/cargo_front
git pull
cd /root/cargo
docker-compose down
docker volume rm cargo_dist_volume
docker-compose up --build -d

echo 'FINISH'
