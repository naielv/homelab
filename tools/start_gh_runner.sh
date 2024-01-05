sudo apt install screen -y
echo 'cd ~/actions-runner && ./run.sh' > /tmp/start_gh_runner__action.sh
screen -dmS gh_runner bash /tmp/start_gh_runner__action.sh
