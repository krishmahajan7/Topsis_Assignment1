import sys
import pandas as pd
import numpy as np

# ---------- ERROR FUNCTION ----------
def error(msg):
    print("Error:", msg)
    sys.exit(1)

# ---------- MAIN TOPSIS FUNCTION ----------
def topsis(input_file, weights, impacts, result_file="results/result.csv"):

    # ---- Handle Streamlit DataFrame or CSV filename ----
    if isinstance(input_file, pd.DataFrame):
        data = input_file.copy()
    else:
        try:
            data = pd.read_csv(input_file)
        except FileNotFoundError:
            error("Input file not found")

    # ---- Check minimum columns ----
    if data.shape[1] < 3:
        error("Input file must contain at least 3 columns")

    alternatives = data.iloc[:, 0]
    matrix = data.iloc[:, 1:].copy()

    # ---- Check numeric values ----
    try:
        matrix = matrix.astype(float).values
    except:
        error("Columns from 2nd to last must contain numeric values only")

    # ---- Convert weights and impacts if passed as strings ----
    if isinstance(weights, str):
        weights = weights.split(',')

    if isinstance(impacts, str):
        impacts = impacts.split(',')

    # ---- Check length match ----
    if len(weights) != matrix.shape[1]:
        error("Number of weights must match number of criteria columns")

    if len(impacts) != matrix.shape[1]:
        error("Number of impacts must match number of criteria columns")

    # ---- Convert weights to float ----
    try:
        weights = np.array(weights, dtype=float)
    except:
        error("Weights must be numeric and separated by commas")

    # ---- Check impacts validity ----
    for imp in impacts:
        if imp not in ['+', '-']:
            error("Impacts must be either + or -")

    impacts = np.array(impacts)

    # ---------- TOPSIS STEPS ----------

    # Step 1: Normalize matrix
    norm = np.sqrt((matrix ** 2).sum(axis=0))
    normalized = matrix / norm

    # Step 2: Weighted normalization
    weighted = normalized * weights

    # Step 3: Ideal best and worst
    ideal_best = []
    ideal_worst = []

    for j in range(weighted.shape[1]):
        if impacts[j] == '+':
            ideal_best.append(weighted[:, j].max())
            ideal_worst.append(weighted[:, j].min())
        else:
            ideal_best.append(weighted[:, j].min())
            ideal_worst.append(weighted[:, j].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance measures
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Step 5: TOPSIS score
    score = dist_worst / (dist_best + dist_worst)

    # ---- Add results to dataframe ----
    data["Topsis Score"] = score
    data["Rank"] = pd.Series(score).rank(ascending=False)

    # ---- Save result ----
    data.to_csv(result_file, index=False)

    print("TOPSIS calculation completed successfully.")
    print("Result saved in:", result_file)

    return result_file


# ---------- DRIVER CODE FOR CLI ----------
if __name__ == "__main__":

    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputFileName> <Weights> <Impacts> <ResultFileName>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]

    topsis(input_file, weights, impacts, result_file)
