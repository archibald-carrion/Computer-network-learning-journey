# Assignment: Building a Network Dataset for ML

## Objective
Convert raw network packets into a structured CSV dataset suitable for training a Machine Learning classifier.

---

## Tasks

1. Run the generator script to produce:
```

training_data.pcap

```

2. Run the converter script to transform the PCAP into:
```

network_dataset.csv

```

3. Open the CSV file in Excel or a text editor:
- Compare the `mean_len` of the **Chat** label vs the **Video** label.

4. **Critical Thinking**:
- If we added a third flow for **Web Browsing**, how would its `mean_len` and `max_len` differ from Video and Chat?

---

## Feature Engineering Question

In your CSV, we only used packet lengths.

- Name one **temporal feature** (related to time) that you could add to this dataset to help the ML model distinguish between:
- a live video stream  
- a file download
```
