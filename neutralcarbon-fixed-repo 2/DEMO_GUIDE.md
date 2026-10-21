# NeutralCarbon — Demo Guide
How to run the live demo for this project (see also FIXES_APPLIED.md and the viva notes).

## The 7-minute demo flow

## One-time setup — do this THE DAY BEFORE, never on demo morning
```bash
# Python side (from the repo root). NOTE: install the light set below, not
# the full requirements.txt — its TensorFlow Quantum pins can fail on a
# current Mac; the demo path (simulator) does not need them.
python3 -m venv .venv && source .venv/bin/activate
pip install scikit-learn pandas numpy matplotlib sympy pytest

# Blockchain side
cd blockchain && npm install && cd ..
```

## Room setup — 3 terminals + 1 browser tab, all opened BEFORE the panel arrives
- **Terminal 1** (leave running): `cd blockchain && npx hardhat node`
- **Terminal 2**: `cd blockchain` (commands typed here)
- **Terminal 3**: repo root, venv activated (ML commands here)
- **Browser**: `dashboard/index.html` open (double-click the file, or
  `python3 -m http.server 8080` in repo root and open localhost:8080/dashboard/)

## The demo, beat by beat (what to run → what to say)

**Beat 1 — Contracts deploy + credits mint themselves (Terminal 2, ~1 min)**
```bash
npx hardhat run scripts/deploy.js --network localhost
```
Say: "This deploys the ERC-1155 credit contract and the oracle contract,
authorises the oracle as a verifier, and mints three sample credits —
Brazil, Germany, Canada — each starting in PENDING state. A credit is
issued by the contract, but it means nothing until it's verified."

**Beat 2 — Verify → Retire, the heart of the project (Terminal 2, ~1 min)**
```bash
npx hardhat run scripts/demo_verify_retire.js --network localhost
```
Say: "Token 1 is verified — the contract stores the proof hash of the
off-chain screening report, that's the audit link. Then I retire it: all
units are burned, supply goes to zero, status RETIRED. That credit can
never be sold or claimed again — that's how double-counting is prevented."
Point at the three status lines the script prints: PENDING → VERIFIED → RETIRED.

**Beat 3 — The screening layer (Terminal 3, ~2 min)**
Pre-run this before the panel arrives (it takes under a minute; the quantum
simulation is the slow part) and keep the output on screen:
```bash
python ml/honest_evaluate.py --seed 42
```
Say: "Before anything is minted, records are screened. Four classical
detectors plus a simulated quantum feature map, majority vote. There's no
labelled fraud dataset, so evaluation uses seeded synthetic injection —
detectors trained only on data up to 2015, tested on 2016-18. The
autoencoder is our best model at F1 0.51, the ensemble is 0.48, and the
simulated quantum model is honestly our weakest — its circuit parameters
aren't trained yet, and we report that instead of hiding it."
If asked to re-run live: change to `--seed 7` — the ranking stays the same.

**Beat 4 — Dashboard walk-through (Browser, ~2 min)**
Click in this order: emission trends → model comparison (say: "these are
the same numbers you just saw in the terminal — the dashboard renders only
what the evaluation produced") → anomaly list → token ledger (say: "sample
ledger entries for the local prototype") → architecture view.
Footer should read "CSI1006 · VIT 2026 / Ritika Priyadarshni" — if it
doesn't, you're showing the OLD dashboard. Stop and switch to the fixed repo.

**Beat 5 — Close (~30 sec)**
Say: "So the system issues, verifies, transfers and retires carbon credits
under smart-contract control, with a screening layer in front of minting —
and every number in it can be reproduced from a seed. The limitations and
the next step — training the quantum circuit and cross-source consistency
checks — are in Chapter 8 of the report."

## If something breaks live (backup plan, in order)
1. Hardhat node/deploy fails → skip to Terminal 3 + dashboard; say the
   contract lifecycle is also covered by the Hardhat test suite, and show
   `blockchain/deployments/localhost.json` from your rehearsal.
2. Python env fails → show `results/honest_results_seed42.json` (already in
   the repo) + the dashboard, which carries the same numbers.
3. Everything fails → dashboard alone still demos (it's static), plus the
   report's Chapter 7 tables and screenshots. Keep rehearsal screenshots
   on your phone as the last resort.

## Reset between rehearsals
Kill Terminal 1 (Ctrl+C), restart `npx hardhat node` (fresh chain),
delete `blockchain/deployments/localhost.json`, re-run Beat 1 then Beat 2.

## Never during the demo
- Don't open the OLD GitHub repo or old evaluate.py
- Don't say "live Chainlink", "satellite data", "94.2%", or "quantum advantage"
- Don't run `pip install -r requirements.txt` live
- Don't demo on Sepolia/testnet (needs funds + network; localhost is identical bytecode)
