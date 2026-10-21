# Blockchain-Enabled Carbon Credit Tracking: A Smart Contract Approach to Issue, Transfer

**System name: NeutralCarbon** — a prototype for verifiable carbon credit tokenisation on ERC-1155, with a classical ML ensemble and a *simulated* quantum feature map used as a supporting anomaly-screening layer for emission records. No quantum advantage is claimed; all results are reported under the reproducible evaluation protocol in `ml/honest_evaluate.py`.

> CSI1006 Mini Project | VIT Vellore | Semester VL20262701
> > Author: Ritika Priyadarshni (22MIC0018)
> > Supervisor: Dr. Radhakrishna Mohanty, Assistant Professor Sr. Grade 1, SCOPE

---

## Overview

NeutralCarbon integrates **Quantum Machine Learning (QML)**, **classical ML anomaly detection**, and **ERC-1155 blockchain tokenization** to build a transparent, fraud-resistant carbon credit verification system.

```
Data Sources → Preprocessing → ML/QML Anomaly Detection → Chainlink Oracle → Smart Contract → ERC-1155 Tokens
```

---

## Repository Structure

```
NeutralCarbon/  (repository root — all commands below run from here)
├── data/
│   ├── global_emissions.csv          # 92 countries, 1992–2018
│   └── preprocess.py                 # Data cleaning & feature engineering
├── ml/
│   ├── anomaly_detection.py          # Isolation Forest, One-Class SVM, Autoencoder
│   ├── train.py                      # Training pipeline
│   └── evaluate.py                   # Metrics & visualizations
├── quantum/
│   ├── quantum_circuit.py            # TF Quantum / Cirq circuit definition
│   ├── qml_classifier.py             # Quantum ML anomaly classifier
│   └── feature_encoding.py           # Angle encoding of emission features
├── blockchain/
│   ├── contracts/
│   │   ├── CarbonCredit.sol          # ERC-1155 carbon credit token
│   │   └── CarbonOracle.sol          # Chainlink oracle consumer
│   ├── scripts/
│   │   ├── deploy.js                 # Hardhat deploy script
│   │   └── mint.js                   # Token minting script
│   ├── hardhat.config.js
│   └── package.json
├── dashboard/
│   └── index.html                    # Interactive web dashboard
├── tests/
│   ├── test_anomaly.py               # ML unit tests
│   ├── test_quantum.py               # Quantum module tests
│   └── CarbonCredit.test.js          # Smart contract tests
├── docs/
│   └── architecture.md               # System architecture docs
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Python Environment (ML + Quantum)
```bash
git clone https://github.com/Ritika-Sorout/Neutral-carbon-
cd neutralcarbon
pip install -r requirements.txt
```

### 2. Run Anomaly Detection
```bash
python ml/train.py
python ml/evaluate.py
```

### 3. Run Quantum Module (Simulation)
```bash
python quantum/qml_classifier.py
```

### 4. Deploy Smart Contracts
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### 5. Launch Dashboard
```bash
# Simply open dashboard/index.html in a browser
# Or serve with Python:
python -m http.server 8080
# Visit http://localhost:8080/dashboard/
```

---

## Key Results

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Isolation Forest | 84.4% | 0.11 | 0.07 | 0.09 |
| One-Class SVM | 86.2% | 0.36 | 0.46 | 0.41 |
| IQR | 70.3% | 0.21 | 0.68 | 0.32 |
| Autoencoder (MLP) | 87.7% | 0.43 | 0.64 | 0.51 |
| QML (simulated, fixed parameters) | 86.6% | 0.09 | 0.04 | 0.05 |
| Ensemble (majority vote) | 85.9% | 0.38 | 0.64 | 0.48 |

> Evaluation protocol (honest, reproducible — `ml/honest_evaluate.py`, seed 42): temporal split train <=2015 / test 2016-2018, detectors fitted on train only, ground truth = seeded 10% synthetic anomaly injection (magnitude spike / source swap / single-source spike), n_test=276, injected=28. Accuracy is misleading at 10% prevalence; read precision/recall/F1. No quantum advantage is claimed: the QML module is a classical simulation with fixed (untrained) variational parameters.

---

## Tech Stack

- **ML**: scikit-learn, TensorFlow, PyTorch
- **Quantum**: TensorFlow Quantum, Cirq, PennyLane
- **Blockchain**: Solidity, Hardhat, Ethers.js, Chainlink
- **Data**: pandas, numpy, matplotlib, seaborn, plotly
- **Testing**: pytest, Hardhat Mocha

---

## References

1. Zeng et al. (2022) — ML-based anomaly detection for environmental monitoring
2. Havlíček et al. (2019) — Supervised learning with quantum-enhanced feature spaces
3. Ethereum Foundation — ERC-1155 Multi-Token Standard
4. Chainlink Labs — Decentralized Oracle Networks
5. Chandola et al. (2009) — Anomaly Detection: A Survey

---

## License

MIT License — see `LICENSE` file.
