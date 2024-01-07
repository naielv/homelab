echo PLEASE ONLY RUN ON A CLEAN HOST
echo YOU ARE WARNED
curl -fsSL get.docker.com | sh
sudo usermod -aG docker $USERNAME
sudo apt install mergerfs
sudo mkdir -p /mnt/disk{00,01,02,03}
sudo mkdir -p /mnt/storage
sudo chmod -R 777 /mnt
sudo chown -R $USERNAME:$USERNAME /mnt
sudo cat <<EOF >> /etc/fstab
LABEL=DISK00 /mnt/disk00 ext4 rw,relatime 0 0
LABEL=DISK01 /mnt/disk01 ext4 rw,relatime 0 0
LABEL=DISK02 /mnt/disk02 ext4 rw,relatime 0 0
LABEL=DISK03 /mnt/disk03 ext4 rw,relatime 0 0
/mnt/disk* /mnt/storage fuse.mergerfs defaults,nonempty,allow_other,use_ino,cache.files=off,moveonenospc=true,category.create=mfs,dropcacheonclose=true,minfreespace=50G,fsname=mergerfs 0 0
EOF
sudo mount -av
echo Done, please rerun all config.yml-related workflows