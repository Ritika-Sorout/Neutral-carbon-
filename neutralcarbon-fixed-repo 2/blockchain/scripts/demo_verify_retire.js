/**
 * demo_verify_retire.js — NeutralCarbon viva demo, steps 2-3
 * -----------------------------------------------------------
 * After deploy.js has run on localhost (it mints 3 sample credits),
 * this script takes token #1 through the rest of its lifecycle:
 *
 *   PENDING --verifyCredit(proofHash)--> VERIFIED
 *   VERIFIED --retireCredit(all units)--> RETIRED (units burned)
 *
 * Usage (Terminal 2, while `npx hardhat node` runs in Terminal 1):
 *   npx hardhat run scripts/demo_verify_retire.js --network localhost
 *
 * The deployer account is the initial verifier (see CarbonCredit
 * constructor), so no extra setup is needed. The proof hash below is
 * a stand-in for the SHA-256 of the off-chain screening report that
 * ml/honest_evaluate.py produces — in the demo, say exactly that.
 */
const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

const STATUS = ["PENDING", "VERIFIED", "RETIRED", "REVOKED"];

async function show(cc, tokenId, label) {
  const c = await cc.getCredit(tokenId);
  const supply = await cc.totalSupply(tokenId);
  console.log(
    `  ${label.padEnd(28)} status=${STATUS[Number(c.status)]}  ` +
    `country=${c.country}  tonnes=${c.tonnesCO2}  supply=${supply}`
  );
  return c;
}

async function main() {
  const network = hre.network.name;
  const p = path.join(__dirname, `../deployments/${network}.json`);
  if (!fs.existsSync(p)) {
    throw new Error(`No deployment for "${network}". Run deploy.js first.`);
  }
  const deploy = JSON.parse(fs.readFileSync(p, "utf8"));
  const [signer] = await ethers.getSigners();
  const cc = await ethers.getContractAt(
    "CarbonCredit", deploy.contracts.CarbonCredit, signer
  );

  const tokenId = 1; // first sample credit minted by deploy.js (Brazil)
  console.log(`\nNeutralCarbon demo — lifecycle of token #${tokenId}`);
  console.log(`Contract: ${deploy.contracts.CarbonCredit}\n`);

  await show(cc, tokenId, "1. After mint (deploy.js)");

  // Proof hash = stand-in for SHA-256 of the off-chain screening report
  const proofHash = ethers.keccak256(
    ethers.toUtf8Bytes(`neutralcarbon-verification-report-token-${tokenId}`)
  );
  const tx1 = await cc.verifyCredit(tokenId, proofHash, "demo-oracle-request-1");
  await tx1.wait();
  console.log(`  verifyCredit()  proofHash=${proofHash.slice(0, 18)}…  tx=${tx1.hash.slice(0, 12)}…`);
  await show(cc, tokenId, "2. After verifyCredit()");

  const balance = await cc.balanceOf(signer.address, tokenId);
  const tx2 = await cc.retireCredit(tokenId, balance);
  await tx2.wait();
  console.log(`  retireCredit(${balance} units)  tx=${tx2.hash.slice(0, 12)}…`);
  const after = await show(cc, tokenId, "3. After retireCredit()");

  console.log(
    `\n  Supply is now ${await cc.totalSupply(tokenId)} — the retired units are burned` +
    `\n  and can never be transferred or claimed again (double-counting prevented).\n`
  );
  if (Number(after.status) !== 2) {
    throw new Error("Expected final status RETIRED");
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
