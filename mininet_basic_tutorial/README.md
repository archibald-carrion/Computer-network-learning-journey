in Linux install mininet with the following commands:

sudo apt update
sudo apt install mininet openvswitch-switch

test if mininet spin up with
sudo mn


then lets install pox

cd mininet_basic_tutorial
git clone https://github.com/noxrepo/pox.git

cd pox
./pox.py

you should see soemthing like this:
POX 0.7.0 (gar) / Copyright 2011-2020 James McCauley, et al.
WARNING:version:POX requires one of the following versions of Python: 3.6 3.7 3.8 3.9
WARNING:version:You're running Python 3.12.
WARNING:version:If you run into problems, try using a supported version.
INFO:core:POX 0.7.0 (gar) is up.



we then kill the previous command and run the controller:
./pox.py forwarding.l2_learning


then in the other terminal lets spin up mininet with pox controller:

sudo mn --topo single,3 --mac --switch ovsk --controller remote


sudo mn --topo single,3 --mac --switch ovsk --controller remote,ip=127.0.0.1,port=6633


