#!/bin/bash
sudo apt-get install jq
sudo apt install whiptail

#files path
json_path='docker_sdk_api/assets/paths.json'
env_path='gui/src/environments/environment.ts'
env_prod_path='gui/src/environments/environment.prod.ts'
proxy_path='proxy.json'
networks_path='training_api/assets/networks.json'

# install docker
docker_install(){
    sudo apt-get remove docker docker-engine docker.io
    sudo apt-get update

    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common



    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88

    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    sudo groupadd docker
    sudo usermod -aG docker ${USER}
    docker run hello-world
}

#install docker compose
docker_compose_install(){
    #This will install docker-compose following [https://docs.docker.com/compose/install/]
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
    docker-compose --version
}


#install nvidia docker
nvidia_docker_install(){
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
    sudo apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update
    sudo apt-get install nvidia-docker2
    sudo pkill -SIGHUP dockerd
}

#check if nvidia docker exist if no ask if it should be installed and then install it
check_nvidia_docker(){
    echo 'checking if nvidia-docker2 is installed'
    if [ "$(dpkg -l | grep nvidia-docker)" ]; then
        echo "nvidia-docker2 found" 
    else
        echo "nvidia-docker was not detected do you want to install it?"
        select yn in "Yes" "No"; do
            case $yn in
                Yes ) nvidia_docker_install; break;;
                No ) exit;;
                *) echo "invalid option $REPLY";;
            esac
        done
    fi
}

# change training api image name based on architecture CPU/GPU
change_image_name(){
jq '."image_name"="'$1'"'  "$json_path" >temp.$$.json && mv temp.$$.json "$json_path"
}
# change proxy values 
change_proxy_values(){
    echo Please enter HTTP_PROXY value:
    read proxy_http
    echo Please enter HTTPS_PROXY value:
    read proxy_https
    jq '."HTTP_PROXY"="'$proxy_http'"'  "$proxy_path" >temp.$$.json && mv temp.$$.json "$proxy_path"
    jq '."HTTPS_PROXY"="'$proxy_https'"'  "$proxy_path" >temp.$$.json && mv temp.$$.json "$proxy_path"

    python3 set_proxy_args.py
}
# change proxy to null
change_proxy_null_values(){

    jq '."HTTP_PROXY"=""'  "$proxy_path" >temp.$$.json && mv temp.$$.json "$proxy_path"
    jq '."HTTPS_PROXY"=""'  "$proxy_path" >temp.$$.json && mv temp.$$.json "$proxy_path"
    python3 set_proxy_args.py
}
#change ip address in environment.prod.ts and environment.ts
change_ip(){
    old_url="$(cat $env_path |grep url)"
    old_prod_url="$(cat $env_prod_path |grep url)"
    old_prod_interfaceapi="$(cat $env_prod_path |grep inferenceAPIUrl)"
    old_interfaceapi="$(cat $env_path |grep inferenceAPIUrl)"
    new_url="url : '$1',"
    new_interfaceapi="inferenceAPIUrl: '$2'"
    if [[ $old_url != "" && $new_url != "" ]]; then
        sed -i "s@$old_url@$new_url@gi" $env_path 
        sed -i "s@$old_prod_url@$new_url@gi" $env_prod_path
    fi
    if [[ $old_interfaceapi != "" && $new_interfaceapi != "" ]]; then
        sed -i "s@$old_interfaceapi@$new_interfaceapi@gi" $env_path
        sed -i "s@$old_prod_interfaceapi@$new_interfaceapi@gi" $env_prod_path
    fi
}


adjust_base_dir(){
    #Remove deleteme files
    rm -f checkpoints/.gitkeep
    rm -f checkpoints/servable/.gitkeep
    rm -f inference_api/models/.gitkeep
    rm -f tensorboards/.gitkeep

    #Adjust basedir path
    python3 adjust_basedir_path.py
}

CPU_docker_image="tf2_training_api_cpu"
GPU_docker_image="tf2_training_api_gpu"
#check docker
echo '----------------------------------------------'
echo 'checking if docker is installed'
if [ -x "$(command -v docker)" ]; then
    echo "docker found" 
else
    echo "Docker was not detected do you want to install it?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) docker_install; break;;
            No ) exit;;
            *) echo "invalid option $REPLY";;
        esac
    done
fi
echo '----------------------------------------------'
#check docker-compose
echo 'checking if docker-compose is installed'
if [ -x "$(command -v docker-compose)" ]; then
    echo "docker-compose found"
else
    echo "Docker-compose was not detected do you want to install it?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) docker_compose_install; break;;
            No ) exit;;
            *) echo "invalid option $REPLY";;
        esac
    done
fi
echo '----------------------------------------------'
echo 'Please choose docker image build architecture'

PS3='Please enter your choice: '
options=("GPU" "CPU")

adjust_base_dir

#CPU/GPU
select opt in "${options[@]}"
do
    case $opt in
        "GPU")
            check_nvidia_docker
            change_image_name "$GPU_docker_image"
            break
            ;;
        "CPU")
            
            change_image_name "$CPU_docker_image"
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

#network interface
echo '----------------------------------------------'
echo "Please select a network interface to setup GUI environment:"
interfaces="$(ls /sys/class/net)"
array=( $interfaces )
while true;
do
    echo
    for i in "${!array[@]}";
    do
        output="$(ip -br addr show ${array[$i]})"
        echo "  [$(($i+1))] $output"
    done
    ((i++))
    echo
    read -p "-> " choice
    [ -z "$choice" ] && choice=-1
    if (( "$choice" > 0 && "$choice" <= $i )); then
        item="${array[$(($choice-1))]}"
        echo "interface selected: $item"
        ipadd="$(ip -4 addr show $item | grep -oP '(?<=inet\s)\d+(\.\d+){3}')"
        break
    else
        echo "invalid option"
    fi
done
echo "ip address to be used: $ipadd"
change_ip "http://$ipadd:" "http://$ipadd:4343/docs"

#proxy
echo '----------------------------------------------'
echo "Do you want to set up proxy?"
select yn in "Yes" "No"; do
case $yn in
    Yes ) change_proxy_values; break;;
    No ) change_proxy_null_values; break;;
    *) echo "invalid option $REPLY";;
esac
done

echo '----------------------------------------------'
# select the network to be downloaded and used later
array=($(jq --raw-output 'keys_unsorted | @sh' $networks_path))
string=""
for i in "${array[@]}"
do
    if [ -z "$string" ]
    then
    string="$i '""' OFF"
    else
    string="$string $i '""' OFF"
    fi
done
string=${string//"''"/'""'}
string=${string//"'"/''}

arr=($string)
#set all values to false
temp_path='./temp-network.json'
jq 'if .? then .[]=false else . end' -c  "$networks_path" >"$temp_path"
KEY=$(whiptail --title "Please pick network to be intalled" --checklist \
"Please pick one or more networks to be intalled" 15 60 4 ${arr[@]} 3>&1 1>&2 2>&3)
exitstatus=$?
if [ $exitstatus = 0 ]; then
    keys=($KEY)
    #set selected keys to true
    for i in "${keys[@]}"
    do
        jq '.'$i'='true''  "$temp_path" >temp.$$.json && mv temp.$$.json "$temp_path"
    done
    mv "$temp_path" "$networks_path"
    echo "You've successfully completed the environment setup."
else
    echo "You chose Cancel."
fi
