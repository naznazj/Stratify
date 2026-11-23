#!/usr/bin/env node

/**
 * STRATIFY CLI & Skill Loader
 * Run via npx:
 *   npx stratify-ai Healthcare --location Philippines
 *   npx stratify-ai --web
 *   npx stratify-ai --install-skill
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const rootDir = path.resolve(__dirname, '..');
const args = process.argv.slice(2);

// Banner
function printBanner() {
  console.log(`
  ____ _____ ____      _  _____ ___ _______   __
 / ___|_   _|  _ \\    / \\|_   _|_ _|  ___\\ \\ / /
 \\___ \\ | | | |_) |  / _ \\ | |  | || |_   \\ V / 
  ___) || | |  _ <  / ___ \\| |  | ||  _|   | |  
 |____/ |_| |_| \\_\\/_/   \\_\\_| |___|_|     |_|  
                                                
 STRATIFY — Business Intelligence & Strategic Marketing Engine
`);
}

// 1. Skill Auto-Installer for AI Agent environments
if (args.includes('--install-skill')) {
  printBanner();
  console.log('[INSTALL] Installing STRATIFY Skill into AI Agent directories...\n');

  const homeDir = os.homedir();
  const potentialSkillDirs = [
    path.join(homeDir, '.gemini', 'antigravity', 'skills', 'stratify'),
    path.join(homeDir, '.agent', 'skills', 'stratify'),
    path.join(homeDir, '.cursor', 'skills', 'stratify')
  ];

  let installedCount = 0;
  for (const target of potentialSkillDirs) {
    const parentDir = path.dirname(target);
    if (!fs.existsSync(parentDir)) {
      try {
        fs.mkdirSync(parentDir, { recursive: true });
      } catch (e) {}
    }

    if (fs.existsSync(parentDir) && !target.startsWith(rootDir)) {
      try {
        fs.mkdirSync(target, { recursive: true });
        fs.cpSync(rootDir, target, {
          recursive: true,
          filter: (src) => !src.includes('node_modules') && !src.includes('.git') && !src.includes('skills/stratify')
        });
        console.log(`[SUCCESS] Installed STRATIFY skill to: ${target}`);
        installedCount++;
      } catch (err) {
        console.log(`[WARNING] Could not copy to ${target}: ${err.message}`);
      }
    }
  }

  if (installedCount === 0) {
    console.log(`[INFO] STRATIFY is ready. You can copy this folder to any agent skills directory.`);
  }

  console.log('\n[COMPLETE] Installation finished. You can now use /stratify [industry] in your AI agent.');
  process.exit(0);
}

// 2. Launch Web Dashboard
if (args.includes('--web') || args.includes('-w') || args.includes('serve')) {
  printBanner();
  console.log('[SERVER] Starting STRATIFY Web Server on http://127.0.0.1:8000...\n');

  const pythonCmd = getPythonCommand();
  if (!pythonCmd) {
    console.error('[ERROR] Python 3 is required to run the backend server.');
    process.exit(1);
  }

  const serverProcess = spawn(pythonCmd, [path.join(rootDir, 'server.py')], {
    cwd: rootDir,
    stdio: 'inherit'
  });

  serverProcess.on('error', (err) => {
    console.error(`Failed to start server: ${err.message}`);
  });
  return;
}

// 3. Run STRATIFY Command via CLI
printBanner();

const pythonCmd = getPythonCommand();
if (!pythonCmd) {
  console.error('❌ Python 3 is required. Please install Python 3.10+ to run the research orchestrator.');
  process.exit(1);
}

// Build argument string
let commandArg = args.join(' ');
if (!commandArg || commandArg.trim() === '') {
  commandArg = '--repl';
} else if (!commandArg.startsWith('/stratify') && !commandArg.startsWith('stratify') && !commandArg.startsWith('-')) {
  commandArg = `/stratify ${commandArg}`;
}

const child = spawn(pythonCmd, [path.join(rootDir, 'stratify.py'), commandArg], {
  cwd: rootDir,
  stdio: 'inherit'
});

child.on('exit', (code) => {
  process.exit(code || 0);
});

function getPythonCommand() {
  for (const cmd of ['python', 'python3', 'py']) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {
      // Continue
    }
  }
  return null;
}
