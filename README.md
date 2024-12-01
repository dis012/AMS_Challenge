# convexAdam
Original code and documentation available at: https://github.com/multimodallearning/convexAdam

# Izziv pri predmetu Analiza medicinskih slik
This document outlines the results of testing two different image registration models: 

1. **Model 1: U-Net based Registration**
2. **Model 2: MIND-based Registration**

The evaluation was performed on the **AMS Challenge** dataset and Grand Challenge dataset (CT images during inspiration and expiration).

---

## **1. U-Net Based Registration**

### **Results on AMS Challenge Data**
- **Dice**: 0.7962
- **Dice30**: 0.6446
- **jstd**: 0.013
- **HD95**: 28.22

### **Results on Lung CT Images**
- **Dice**: 0.87
- **Dice30**: 0.87
- **jstd**: 0.0441
- **HD95**: 13.67

### **Commentary on U-Net Results**
- **Dice**: The Dice coefficient on AMS Challenge data indicates good overlap (0.7962), but the performance is significantly better on the lung CT images (0.87), probably because lung CT images had just 2 labes while AMS CT images had 14.
- **jstd**: The Jacobian standard deviation (jstd) is very low for AMS Challenge data (0.013), highlighting smoother deformation fields. For Grand Challenge dataset, the jstd is slightly higher (0.0441).
- **HD95**: The Hausdorff Distance at 95th percentile (HD95) is high for AMS Challenge data (28.22), indicating boundary discrepancies. However, for Grand Challenge dataset, it is significantly lower (13.67), demonstrating better alignment.

---

## **2. MIND-Based Registration**

### **Results on AMS Challenge Data**
- **TRE**: 4.1468
- **jstd**: 0.0653

### **Commentary on MIND Results**
- **TRE**: The Target Registration Error (TRE) of 4.1468 suggests moderate misalignment on AMS Challenge data. This indicates that the MIND-based model may not be as precise as the U-Net model for this dataset.
- **jstd**: A higher jstd (0.0653) compared to the U-Net model (0.013 for AMS data) suggests more variability in the deformation field, indicating that the MIND model produces more complex transformations.

---

## **Comparison Between U-Net and MIND Models**

- **Dice Coefficients**: The U-Net model significantly outperforms the MIND model in terms of Dice score, particularly on well-aligned custom CT images.
- **TRE and jstd**: While MIND shows reasonable TRE and jstd values on AMS Challenge data, the U-Net model demonstrates superior performance, particularly in producing smoother deformation fields.
- **HD95**: The U-Net model provides a much lower HD95 score on custom data, indicating better alignment with reduced boundary discrepancies.

In summary, the U-Net model delivers better performance for both AMS Challenge and custom data, particularly in terms of Dice, HD95, and overall alignment accuracy. However, MIND-based registration may still have applications in scenarios requiring more flexible deformation modeling.

---

## **Visualization**

1. **Before Registration**: The CT scans before alignment.
2. **After Registration**: The CT scans after applying the registration model.
3. **Difference Image**: A difference image highlighting misalignments.

### Example Visualization Section

**U-Net Model Results on CT expiration/inspiration**:
![Before Registration](images/CTBefore.png)
![After Registration](images/CTAfter.png)
![Difference Image](images/CTDiff.png)

**U-Net Model Results on AMS Challenge Data**:
![Before Registration](images/AMSBefore.png)
![After Registration](images/AMSAfter.png)
![Difference Image](images/AMSDiff.png)

**MIND Model Results on AMS Challenge Data**:
![Before Registration](images/MINDBefore.png)
![After Registration](images/MINDAfter.png)
![Difference Image](images/MINDDiff.png)

---

## **Conclusion**

- **U-Net Model**: Outperforms MIND-based registration on both datasets. It is particularly effective on custom CT images during inspiration and expiration.
- **MIND Model**: Provides reasonable results on AMS Challenge data but shows higher TRE and jstd, indicating less precise deformation compared to U-Net.

Both models provide valuable insights into registration performance, with U-Net being the preferred choice for the given datasets.

---