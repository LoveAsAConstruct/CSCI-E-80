import csv
import sys
import calendar
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

TEST_SIZE = 0.4
REVERSE_MONTH_DICT = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4,
    "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9,
    "Nov": 10, "Dec": 11
}
def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename, newline='') as file:
        file_content = csv.reader(file)
        next(file_content)  # Skip the first row
        for row in file_content:
            # Convert all data to numerics which are added to training data
            row_evidence = [convert_to_numeric(i, cell) for i, cell in enumerate(row[:-1])]
            evidence.append(row_evidence)
            labels.append(1 if row[-1] == 'True' else 0)
    return (evidence, labels)

def convert_to_numeric(index, value):
    # Seperates input values into varying datatypes represented as a float or int
    if index in [0, 2, 4, 11, 12, 13, 14]: 
        return int(value)
    elif index in [1, 3, 5, 6, 7, 8, 9]:
        return float(value)
    elif index == 10: 
        return REVERSE_MONTH_DICT[value]
    elif value == "Returning_Visitor":
        return 1
    elif value == "New_Visitor":
        return 0
    elif value == "Other":
        return 0.5 # This one was funky, there was no mention of "Other" exept for in the source data, so I gave it middleground
    elif value in ['True', 'False', 'TRUE', 'FALSE']:  
        return 1 if value == 'True' or value == 'TRUE' else 0
    
def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
|    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Scale the features to normalize
    scaler = StandardScaler()
    scaled_evidence = scaler.fit_transform(evidence)
    
    # Use classifier with n=1
    knn = KNeighborsClassifier(n_neighbors=1)
    
    # Return model
    return knn.fit(scaled_evidence, labels)

TRUE = 1
FALSE = 0
def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Get predictions and labels in numpy array objects
    predictions = np.array(predictions)
    labels = np.array(labels)

    # Calculate true positives and negatives as points where predictions and labels are the same value
    true_positives = np.sum((predictions == 1) & (labels == 1))
    true_negatives = np.sum((predictions == 0) & (labels == 0))
    
    # Calculate total positives and negatives based on label value
    total_positives = np.sum(labels == 1)
    total_negatives = np.sum(labels == 0)
    sensitivity = true_positives / total_positives if total_positives > 0 else 0
    specificity = true_negatives / total_negatives if total_negatives > 0 else 0
    
    # Return values
    return sensitivity, specificity


if __name__ == "__main__":
    main()
