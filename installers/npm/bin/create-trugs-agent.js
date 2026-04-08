#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const TEMPLATES = path.join(__dirname, "..", "templates");
const DEST = process.cwd();

const args = process.argv.slice(2);
const ide = args[0] || "claude";

const IDE_FILES = {
  claude: "CLAUDE.md",
  cursor: ".cursorrules",
  copilot: ".github/copilot-instructions.md",
};

const targetFile = IDE_FILES[ide];
if (!targetFile) {
  console.error(`Unknown IDE: ${ide}`);
  console.error("Usage: npx create-trugs-agent [claude|cursor|copilot]");
  console.error("Default: claude");
  process.exit(1);
}

// Copy AGENT.md as the IDE-specific file
const agentSrc = path.join(TEMPLATES, "AGENT.md");
const agentDest = path.join(DEST, targetFile);

// Create parent directory if needed (for .github/copilot-instructions.md)
const parentDir = path.dirname(agentDest);
if (!fs.existsSync(parentDir)) {
  fs.mkdirSync(parentDir, { recursive: true });
}

if (fs.existsSync(agentDest)) {
  console.log(`${targetFile} already exists — skipping (won't overwrite)`);
} else {
  fs.copyFileSync(agentSrc, agentDest);
  console.log(`Created ${targetFile}`);
}

// Copy component folders
const components = [
  "AAA",
  "EPIC",
  "FOLDER",
  "MEMORY",
  "SKILLS",
  "TRUGGING",
  "WEB_HUB",
];

let copied = 0;
for (const comp of components) {
  const srcDir = path.join(TEMPLATES, comp);
  if (!fs.existsSync(srcDir)) continue;

  const destDir = path.join(DEST, comp);
  if (fs.existsSync(destDir)) {
    console.log(`${comp}/ already exists — skipping`);
    continue;
  }

  copyDir(srcDir, destDir);
  copied++;
  console.log(`Created ${comp}/`);
}

// Copy validator
const toolsSrc = path.join(TEMPLATES, "tools");
const toolsDest = path.join(DEST, "tools");
if (fs.existsSync(toolsSrc) && !fs.existsSync(toolsDest)) {
  copyDir(toolsSrc, toolsDest);
  console.log("Created tools/ (validator)");
}

console.log(
  `\nTRUGS Agent initialized for ${ide}. Your LLM now speaks TRL.`
);
console.log(`  ${targetFile} — TRL vocabulary and grammar`);
if (copied > 0) {
  console.log(`  ${copied} component folders — methodology and tools`);
}
console.log("\nFull docs: https://github.com/TRUGS-LLC/TRUGS-AGENT");

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}
