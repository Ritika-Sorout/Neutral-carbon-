# FIXES_APPLIED — NeutralCarbon anomaly fix log (2026-10-21)
Fixed copy prepared for: Ritika Priyadarshni (22MIC0018), CSI1006 Mini Project,
Guide: Dr. Radhakrishna Mohanty, Assistant Professor Sr. Grade 1, SCOPE.
Registered title: "Blockchain-Enabled Carbon Credit Tracking: A Smart Contract
Approach to Issue, Transfer [TITLE CONTINUES — update here when full title is confirmed]"

## Identity / course anomalies — FIXED
1. `README.md` header: BCSE498J Project-II / Kiran Tripathy (22BDS0172) /
   Kolangada Advaith Dilip (22BCE0772) / Prof. Akila Victor
   → CSI1006 Mini Project, Ritika Priyadarshni (22MIC0018), Dr. Radhakrishna Mohanty.
   (The duplicate nested README no longer exists — see structure fix #9.)
2. `dashboard/index.html` sidebar footer: "BCSE498J · VIT 2026 / Kiran · Advaith"
   → "CSI1006 · VIT 2026 / Ritika Priyadarshni". Re-take all dashboard screenshots
   AFTER this fix.
3. `blockchain/contracts/CarbonCredit.sol` + `CarbonOracle.sol` header comments:
   other authors → Ritika Priyadarshni (22MIC0018), CSI1006 Mini Project.
4. README title/framing: "Quantum-Enhanced … Fraud Detection" → registered title,
   with ML/QML described honestly as a supporting screening layer, simulation-level,
   no quantum-advantage claim.
5. Clone URL placeholder `YOUR_USERNAME/neutralcarbon.git` → `Ritika-Sorout/Neutral-carbon-`.

## Results / claims anomalies — FIXED
6. The 94.2% QML table (was in README, docs/architecture.md, dashboard ×4):
   replaced everywhere with the honest seeded-injection results (seed 42):
   IF 84.4/0.09, OC-SVM 86.2/0.41, IQR 70.3/0.32, Autoencoder 87.7/0.51,
   Simulated QML 86.6/0.05, Ensemble 85.9/0.48 (accuracy/F1). Dashboard model
   metrics + performance chart now use the same numbers, chart axis rescaled 60–100.
   Reproduce: `python ml/honest_evaluate.py --seed 42` (also `--seed 7`).
7. IQR inconsistency: dashboard showed IQR 82.3%/0.81 while README omitted IQR.
   Both now show IQR from the same honest run.
8. Fake satellite claim: "Copernicus Sentinel" removed from
   `docs/architecture.md` (oracle audit-trail bullet) and `dashboard/index.html`
   (architecture diagram + data-source line). Data source is reported emission
   records (country-level dataset) — nothing else.
9. `ml/evaluate.py`: REMOVED (a) training on the full dataset including test
   years (leakage) and (b) the 8 hard-coded large-emitter "ground truth".
   `make_ground_truth()` now raises with an explanation; evaluation delegates
   to `ml/honest_evaluate.py`. NOTE: `ml/train.py` was checked and was already
   correct (proper temporal split) — unchanged.

## Structure / reproducibility anomalies — FIXED
10. Nested layout: code was buried in `BLOCKCHAIN_CARBON/neutral_carbon/` with
    only a README + LICENSE at repo root, so Quickstart commands failed from
    root. This copy is FLATTENED: `data/ ml/ quantum/ blockchain/ dashboard/
    tests/` sit at the root, and all README commands run from here.
11. Missing `.github/workflows/ci.yml` (claimed in README structure): created —
    Python tests (pytest) + Hardhat compile jobs.
12. Dashboard chart randomness: scatter + noise charts used `Math.random()`,
    so every page load showed different "results". Replaced with a seeded
    mulberry32 PRNG (seed 42). Remaining `Math.random()` uses are only in
    simulated transaction-ID generation for the demo mint interaction, which
    is supposed to differ per transaction. Sample ledger arrays are now
    labelled in-code as DEMO data for the local Hardhat prototype.
13. Docstring mismatches: `quantum/feature_encoding.py` listed an
    "AmplitudeEncoding" that doesn't exist — removed. `quantum/qml_classifier.py`
    said "9 emission features → PCA" — corrected to the actual 15-feature pipeline.

## NOT fixed here — needs you
A. Full registered title: your screenshot ends mid-title at "Transfer".
   Update the title in: this file, `README.md` line 1, report cover /
   declaration / certificate, once you send the full title.
B. Git author name: your commits are authored "Ritika Piyadarshni Sorout"
   (misspelled Priyadarshni). Fix for future commits:
   `git config --global user.name "Ritika Priyadarshni"` — past commit history
   and the GitHub username (Ritika-Sorout) are not changed by this.
C. GitHub push: this is a fixed local copy. To publish: replace the contents
   of your GitHub repo with this folder's contents (keep the repo URL), or
   create a fresh repo from this folder. Do not push until (A) is done.
D. Test status (verified 2026-10-21): Python suite = 50 passed, 3 FAILED —
   all three in tests/test_quantum.py (test_anomaly_higher_than_normal,
   test_different_seeds_give_different_scores, test_flags_and_scores_consistent).
   The identical 3 failures occur on the ORIGINAL untouched code, so they are
   pre-existing, not caused by these fixes: the tests assert that the simulated
   quantum classifier separates anomalies, but its variational parameters are
   fixed/random, so it does not. Do NOT silently edit the tests to pass —
   either train the parameters (future work) or present the failures as
   evidence for the negative QML result in the report (Ch. 7.3).
   Hardhat contract tests were not re-run in this fix session. Run
   `cd blockchain && npm install && npx hardhat test` once locally before the viva demo.
E. Bonafide-work declaration: this package fixes names and framing. The
   declaration decision (what is your own build on top of the base code)
   stays between you and Dr. Mohanty — see the note in the chat.
