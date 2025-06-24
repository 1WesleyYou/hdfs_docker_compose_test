#!/bin/bash

sudo apt-get update 

sudo apt-get install autoconf automake libtool curl make g++ unzip python3-pip -y
sudo apt-get install ninja-build gettext cmake curl build-essential fish -y

sudo apt-get install -y git maven ant vim openjdk-8-jdk golang-go gnuplot zsh
sudo update-alternatives --set java $(sudo update-alternatives --list java | grep "java-8")

pip install -r requirements.txt

export JAVA_HOME=$(/usr/lib/jvm/java-8-openjdk-amd64) 
export PATH=$JAVA_HOME/bin:$PATH

# cd neovim || exit 1
# make CMAKE_BUILD_TYPE=RelWithDebInfo
# sudo make install 
# printf "[\033[0mINFO\033[0m] Neovim installed successfully."

sudo chsh -s /usr/bin/fish

# git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim
# rm -rf ~/.config/nvim/.git
# git clone https://github.com/1WesleyYou/personal_configs.git
# cp -r personal_configs/nvim/* ~/.config/nvim/
# cp nvim/nvim /usr/local/bin/nvim
# cp -r nvim ~/.config

cd ~ || exit 1

# cd protobuf-2.5.0
#
# ./configure
#
# make 
#
# make check
#
# sudo make install

# sudo cp dll/protoc /usr/local/bin/ 
# sudo chmod +x /usr/local/bin/protoc

# sudo cp -r dll/* /usr/local/lib/
wget https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip
unzip protobuf-2.5.0.zip
cd protobuf-2.5.0 || exit 1
./configure
make
make check
sudo make install
sudo ldconfig # refresh shared library cache.

echo -e "[\033[0mINFO\033[0m] Protobuf installed successfully."

cd ~ 

git clone https://github.com/apache/hadoop.git 

# cd hdfs_docker_compose_test/hdfs_16633 || exit 1

# ./hdfs_16633_install.sh "$(pwd)/../../hadoop"