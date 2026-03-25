# Assignment: Building a Network Dataset for ML

## Objective
Convert raw network packets into a structured CSV dataset suitable for training a Machine Learning classifier.

---

## Tasks

1. Run the generator script to produce: `training_data.pcap`

2. Run the converter script to transform the PCAP into: `network_dataset.csv`

3. Open the CSV file in Excel or a text editor. Compare the `mean_len` of the **Chat** label vs the **Video** label.
    79.93939393939394 vs 1469.6666666666667

4. **Critical Thinking**: If we added a third flow for **Web Browsing**, how would its `mean_len` and `max_len` differ from Video and Chat?
    I think this would be quite similar to the chat in term of ratio, until a moment where the flow probably would "explode", like burst of data, if I had to guess I would say that it will be more chaotic with variety of size.

---

## Feature Engineering Question

In your CSV, we only used packet lengths. Name one 'Temporal' feature (related to time) that you could add to this dataset to help the ML model distinguish between a live video stream and a file download.
A useful temporal feature is inter-arrival time between packets, as live video streams tend to have consistent packet timing, while file downloads exhibit brust of traffic with variable delays between packets.