# ultra basic ML based SDNM 

The objective of this small project is to build a model whjich is able to detect and block network flows that contain a higher-than-expected volume of data. For example, a standard ping running between two nodes (Node A and Node B) should not cause any issues and the traffic should be allowed. However, if a node attempts a ping flood—sending many simultaneous packets—then that connection must be blocked.

The steps to take are:
1. **Train a model** (any model of choice) using the dataset provided (flow_Dataset.csv). This dataset includes both normal-volume and high-volume traffic.
2. **Export** the trained model.
3. **Import** the model into a POX controller module that extracts flow statistics from a switch and handles the feature extraction.



Once the model build with python basic_decision_Tree.py or any other model you whish to make, just move ml_traffic_DEtector_hints.py and your .pkl to /pox/ext

pox/
├── pox.py
├── ext/
│   ├── ml_detector.py
│   └── traffic_model.pkl
├── pox/
├── tests/
└── ...


python3 -m venv .venv
source .venv/bin/activate

first spin up pox:
./pox.py forwarding.l2_learning ml_traffic_detector_hints


andi n another terminal spin up mininet:



to test:
h2 iperf -s &
h1 iperf -c 10.0.0.2 --> this one also did large average size which triggered my first tree
h1 ping -s 1472 -i 0.001 h2 --> to try packets with a flow with a high er packets average size (this one happened to be the one detected with my first tree)
 h1 ping -f h2 --> to try high frequence little packets 


### Deliverables

You must submit a **single PDF** including the following:

* An explanation of what had to be added to the code to achieve the required functionality.
* A screenshot of the new code (it is not necessary to show the entire file).
* A screenshot proving that the traffic is successfully being blocked.



the dataset is a training dataset for the ml model

after generating it i should use the given ml_traffic_detector_hints.py to filter ping (dos simulation in this scenario) in mininet

first you will need to follow the previous tutorial to setup mininet and pox in you environment