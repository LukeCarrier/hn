#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.0.img ] && scp dev.ossservices.com:/srv/centos-6.0.img.gz . && echo "Downloading the image" && gunzip centos-6.0.img.gz


# Run the build system
echo "Launch the VM to build HyperNova Package: will be use for the build AND the client"
qemu-img create -f qcow2 -b centos-6.0.img target.img 

echo "Running emulator. You can ssh into it from the port 2222"
qemu-system-x86_64 -m 512 -net nic -net user -hda target.img  -enable-kvm -redir tcp:2222::22

# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

