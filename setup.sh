#!/bin/bash

sudo apt-get update

sudo apt-get install autoconf automake libtool curl make g++ unzip
sudo apt-get install ninja-build gettext cmake curl build-essential

sudo apt-get install -y git maven ant vim openjdk-8-jdk golang-go gnuplot zsh
sudo update-alternatives --set java $(sudo update-alternatives --list java | grep "java-8")
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/neovim/neovim
cd neovim 
git checkout stable
make CMAKE_BUILD_TYPE=RelWithDebInfo
sudo make install 
echo "[\033[0mINFO\033[0m] Neovim and Oh-My-Zsh installed successfully."

wget fish_4.0.2-2~jammy_amd64.deb
sudo dpkg -i fish_4.0.2-2~jammy_amd64.deb
sudo chsh -s /usr/bin/fish

git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim
rm -rf ~/.config/nvim/.git
git clone https://github.com/1WesleyYou/personal_configs.git
cp -r personal_configs/nvim/* ~/.config/nvim/

cd ~

wget https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip

unzip protobuf-2.5.0.zip
cd protobuf-2.5.0

./configure

make 

make check

sudo make install

sudo ldconfig

echo -e "[\033[0mINFO\033[0m] Protobuf installed successfully."

cd ~ 

git clone https://github.com/apache/hadoop.git
cd hadoop
git checkout rel/release-3.1.3

mvn clean package -Pdist -DskipTests -Dtar

cd ~

git clone https://github.com/OrderLab/T2C.git

cd T2C

touch build_hdfs_t2c.sh

echo > "build_hdfs_t2c.sh" << EOF
# change variable value according to folder location
hdfs_dir=/users/yuchenxr/hadoop
t2c_dir=/users/T2C
script_dir=${t2c_dir}/conf/scripts/hdfs
version=3.1.3

cd $hdfs_dir
# checkout to buggy version of hdfs
git checkout tags/rel/release-3.1.3

cd $t2c_dir

# compile t2c
./run_engine.sh compile

# apply patch
./run_engine.sh patch conf/samples/hdfs-3.1.3.properties hdfs

# build system
./run_engine.sh recover_tests conf/samples/hdfs-3.1.3.properties

# hdfs needs to apply patch again after recover
./run_engine.sh patch conf/samples/hdfs-3.1.3.properties hdfs

# copy config files
cp $script_dir/core-site.xml hadoop-dist/target/hadoop-${version}/etc/hadoop/
cp $script_dir/hdfs-site.xml hadoop-dist/target/hadoop-${version}/etc/hadoop/
<< EOF
