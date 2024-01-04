sudo apt install screen -y
echo 'cd ~/actions-runner && ./run.sh' > /tmp/start_gh_runner__action.sh
screen -dmS gh_runner bash /tmp/start_gh_runner__action.sh
# wget https://raw.githubusercontent.com/naielv/homelab/main/tools/start_gh_runner.sh?token=GHSAT0AAAAAACMK4IQ7RBV6ORTDJZRP6DOWZMW7ZVA && mv start_gh_run* start_gh_runner.sh && sh start_gh_runner.sh