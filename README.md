# Co2-Emissions-Forecasting-Using-Regression
Implemented a research paper on regression analysis from scratch to predict Co2 emissions of different vehicles.
![Reseach paper Link]()


This repository contains a machine learning project to predict CO2 emissions using multiple regression models, including:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- K-Nearest Neighbors (KNN) Regressor
- XGBoost Regressor



## **Preprocessing Steps**

1. **Handling Missing Values**:
   - Checked for missing data and filled or dropped values as necessary.

2. **Feature Engineering**:
   - Created derived features such as `Fuel Consumption per Cylinder` and `CO2 per Liter`.
   - Combined redundant features like city and highway fuel consumption.

3. **Feature Scaling**:
   - Standardized numerical features for models sensitive to scaling (e.g., KNN, SVR).

4. **Categorical Encoding**:
   - Used one-hot encoding for categorical features like `Transmission` and `Fuel Type`.

5. **Train-Test Split**:
   - Split the dataset into 80% training and 20% testing sets.



## **Model Accuracies**

| Model               | Accuracy (%) |
|----------------------|--------------|
| Random Forest        | **99.67**    |
| K-Neighbors Algorithm| 99.11        |
| Linear Regression    | 99.03        |
| Decision Tree        | 98.23        |
| XGBRegressor         | 84.16        |



## **Visualization**

Below is a bar graph comparing the accuracies of the models:

![Algorithm vs Accuracy](https://github.com/Laasyakshara25/Co2-Emissions-Forecasting-Using-Regression/blob/main/assets/algorithm_vs_accuracy.png)



## **How to Use**
 Clone this repository:
   ```bash
   git clone https://github.com/Laasyakshara25/Co2-Emissions-Forecasting-Using-Regression.git
   ```
