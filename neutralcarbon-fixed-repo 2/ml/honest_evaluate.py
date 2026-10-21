"""
honest_evaluate.py — NeutralCarbon (MARKS-FIX version)
-------------------------------------------------------
WHY THIS FILE EXISTS
The original ml/evaluate.py used 8 hard-coded (year, country) tuples
(China 2018, India 2017, USA 2015, ...) as "ground truth anomalies".
Those are simply the world's largest emitters, not audited fraud cases,
so every metric derived from them (including the README's 94.2% QML
table) is indefensible in a viva.

THIS EVALUATION IS DEFENSIBLE BECAUSE:
1. Train / test is temporal: train <= 2015, test = 2016-2018 (as original).
2. Detectors are fitted on TRAIN ONLY.
3. Ground truth in test is created by SEEDED SYNTHETIC INJECTION:
   a known fraction (10%) of test rows is perturbed by one of three
   documented operations, and exactly those rows are labelled anomalous.
   This is a standard evaluation protocol for anomaly detection when no
   labelled fraud data exists (Chandola et al., 2009) — and we SAY SO.
4. Every number printed here is reproduced by running this file:
       python ml/honest_evaluate.py --seed 42
   Results are written to results/honest_results_seed<seed>.json + .csv

INJECTION TYPES (each applied to a disjoint subset of injected rows)
  A  magnitude_spike : all CO2 source features x U(2.5, 4.0)
  B  source_swap     : Coal and Oil feature values are interchanged and
                       Cement is replaced by Flaring (composition fraud)
  C  single_source_spike : one randomly chosen source feature x U(4, 6)

LIMITATIONS (state these in the report / viva, do not hide them)
- Synthetic injection measures detection of *injected* perturbations,
  not of real-world carbon-credit fraud, for which no labelled public
  dataset was available for this project.
- The "QML" detector is a NUMPY SIMULATION of a 4-qubit variational
  circuit with FIXED (untrained) variational parameters, followed by a
  classical One-Class SVM. It is not executed on quantum hardware and
  no quantum advantage is claimed.
- The autoencoder here is an MLP autoencoder (scikit-learn
  MLPRegressor, bottleneck architecture) used so the evaluation runs
  without TensorFlow; architecture differs slightly from the TF
  autoencoder described in anomaly_detection.py.
"""

import argparse, json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.preprocess import load_raw, clean, get_feature_matrix, train_test_split_temporal

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "results")
# when run inside the marks-fix pack, results/ sits next to code_fixed/
ALT_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results")

def inject_anomalies(X, seed=42, frac=0.10):
    """Return (X_perturbed, y_true, types) — y_true True exactly on injected rows."""
    rng = np.random.RandomState(seed)
    n = len(X)
    k = max(1, int(round(frac * n)))
    idx = rng.choice(n, size=k, replace=False)
    Xp = X.copy().astype(float)
    y = np.zeros(n, dtype=bool); y[idx] = True
    types = {}
    # feature indices in the scaled matrix correspond to FEATURE_COLS order
    # 0:CH4 1:N2O 2:Cement 3:Coal 4:Gas 5:Oil 6:Flaring 7:Other 8:Total
    thirds = np.array_split(rng.permutation(idx), 3)
    for row in thirds[0]:
        Xp[row, 2:9] *= rng.uniform(2.5, 4.0); types[int(row)] = "A_magnitude_spike"
    for row in thirds[1]:
        Xp[row, 3], Xp[row, 5] = Xp[row, 5], Xp[row, 3]
        Xp[row, 2] = Xp[row, 6]; types[int(row)] = "B_source_swap"
    for row in thirds[2]:
        col = rng.choice([2, 3, 4, 5, 6])
        Xp[row, col] *= rng.uniform(4.0, 6.0); types[int(row)] = "C_single_source_spike"
    return Xp, y, types

def metrics(y_true, y_pred):
    tp = int((y_true & y_pred).sum()); fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum()); tn = int((~y_true & ~y_pred).sum())
    p = tp/(tp+fp) if tp+fp else 0.0; r = tp/(tp+fn) if tp+fn else 0.0
    f1 = 2*p*r/(p+r) if p+r else 0.0; acc = (tp+tn)/len(y_true)
    return dict(accuracy=round(acc,4), precision=round(p,4), recall=round(r,4),
                f1=round(f1,4), tp=tp, fp=fp, fn=fn, tn=tn)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(); seed = args.seed
    df = clean(load_raw())
    X, meta, _ = get_feature_matrix(df)
    # Temporal split by year from meta (train_test_split_temporal in
    # preprocess.py splits a raw DataFrame; here we mask the feature
    # matrix so train and test share one fitted scaler/imputer).
    # NOTE: the original evaluate.py fitted detectors on the FULL data
    # including test years — that leakage is removed here: all detectors
    # below are fit on Xtr only.
    test_mask = meta["Year"].isin([2016, 2017, 2018]).values
    Xtr, Xte = X[~test_mask], X[test_mask]
    print(f"train={len(Xtr)} (<=2015)  test={len(Xte)} (2016-2018)  features={X.shape[1]}")

    Xte_p, y_true, types = inject_anomalies(Xte, seed=seed)
    print(f"injected anomalies: {y_true.sum()} / {len(y_true)}")

    from sklearn.ensemble import IsolationForest
    from sklearn.svm import OneClassSVM
    from sklearn.neural_network import MLPRegressor
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import MinMaxScaler

    results = {}

    # 1) Isolation Forest (fitted on train only)
    iforest = IsolationForest(n_estimators=200, contamination=0.05, random_state=seed)
    iforest.fit(Xtr); results["IsolationForest"] = metrics(y_true, iforest.predict(Xte_p) == -1)

    # 2) One-Class SVM
    ocsvm = OneClassSVM(kernel="rbf", nu=0.05, gamma="scale")
    ocsvm.fit(Xtr); results["OneClassSVM"] = metrics(y_true, ocsvm.predict(Xte_p) == -1)

    # 3) IQR detector (thresholds from train)
    q1, q3 = np.percentile(Xtr, 25, axis=0), np.percentile(Xtr, 75, axis=0)
    iqr = q3 - q1; lo, hi = q1 - 2.5*iqr, q3 + 2.5*iqr
    iqr_flag = ((Xte_p < lo) | (Xte_p > hi)).any(axis=1)
    results["IQR"] = metrics(y_true, iqr_flag)

    # 4) MLP Autoencoder (bottleneck) — reconstruction error, threshold = 95th pct of train
    d = Xtr.shape[1]
    ae = MLPRegressor(hidden_layer_sizes=(64, 32, 16, 32, 64), activation="relu",
                      max_iter=500, random_state=seed)
    ae.fit(Xtr, Xtr)
    err_tr = ((ae.predict(Xtr) - Xtr) ** 2).mean(axis=1)
    thr = np.percentile(err_tr, 95)
    err_te = ((ae.predict(Xte_p) - Xte_p) ** 2).mean(axis=1)
    results["Autoencoder_MLP"] = metrics(y_true, err_te > thr)

    # 5) Simulated QML: PCA(4) -> simulated quantum feature map -> One-Class SVM
    #    (reuses the project's own SimulatedQuantumClassifier; theta fixed, seed 42)
    try:
        from quantum.quantum_circuit import SimulatedQuantumClassifier
        pca = PCA(n_components=4, random_state=seed)
        scaler = MinMaxScaler(feature_range=(-np.pi, np.pi))
        qc = SimulatedQuantumClassifier(n_qubits=4, n_layers=3, seed=42)
        def qfeat(Xin):
            Z = scaler.transform(pca.transform(Xin)) if hasattr(scaler, "scale_") else None
            return np.array([qc.encode_and_measure(x) for x in Z])
        pca.fit(Xtr); scaler.fit(pca.transform(Xtr))
        Qtr, Qte = qfeat(Xtr), qfeat(Xte_p)
        qsvm = OneClassSVM(kernel="rbf", nu=0.05, gamma="scale"); qsvm.fit(Qtr)
        results["QML_simulated"] = metrics(y_true, qsvm.predict(Qte) == -1)
        results["QML_simulated"]["note"] = "numpy simulation, fixed untrained theta, no quantum advantage claimed"
    except Exception as e:
        results["QML_simulated"] = {"error": str(e)}

    # 6) Ensemble majority vote (>=2 of IF / OCSVM / IQR / AE)
    votes = np.column_stack([
        iforest.predict(Xte_p) == -1, ocsvm.predict(Xte_p) == -1,
        iqr_flag, err_te > thr]).sum(axis=1)
    results["Ensemble_majority"] = metrics(y_true, votes >= 2)

    # per-type recall for the ensemble + best single model
    per_type = {}
    for t in sorted(set(types.values())):
        rows = np.array([i for i, tt in types.items() if tt == t])
        per_type[t] = dict(n=int(len(rows)),
                           ensemble_recall=round(float((votes[rows] >= 2).mean()), 4),
                           iforest_recall=round(float((iforest.predict(Xte_p[rows]) == -1).mean()), 4))
    out = dict(seed=seed, train_n=int(len(Xtr)), test_n=int(len(Xte)),
               injected_n=int(y_true.sum()), injection_frac=0.10,
               protocol="temporal split <=2015 / 2016-2018; detectors fit on train only; "
                        "ground truth = seeded synthetic injection (types A/B/C)",
               results=results, per_type_recall=per_type)
    for d in (RESULTS_DIR, ALT_RESULTS_DIR):
        try:
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, f"honest_results_seed{seed}.json"), "w") as f:
                json.dump(out, f, indent=2)
            pd.DataFrame(results).T.to_csv(os.path.join(d, f"honest_results_seed{seed}.csv"))
        except Exception as e:
            print("write failed", d, e)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
