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

  // Deploy project instruction rules (GEMINI.md, CLAUDE.md, AGENTS.md, .cursorrules) into current workspace
  const cwd = process.cwd();
  if (cwd !== rootDir) {
    const bridgeFiles = ['GEMINI.md', 'CLAUDE.md', 'AGENTS.md', '.cursorrules'];
    for (const bf of bridgeFiles) {
      const src = path.join(rootDir, bf);
      const dst = path.join(cwd, bf);
      if (fs.existsSync(src) && !fs.existsSync(dst)) {
        try {
          fs.copyFileSync(src, dst);
          console.log(`[SUCCESS] Configured agent rule: ${bf}`);
        } catch (e) {}
      }
    }
    const localAgentSkill = path.join(cwd, '.agent', 'skills', 'stratify');
    if (!fs.existsSync(localAgentSkill)) {
      try {
        fs.mkdirSync(localAgentSkill, { recursive: true });
        fs.copyFileSync(path.join(rootDir, 'SKILL.md'), path.join(localAgentSkill, 'SKILL.md'));
        console.log(`[SUCCESS] Configured workspace skill: .agent/skills/stratify/SKILL.md`);
      } catch (e) {}
    }
  }

  console.log('\n[COMPLETE] Installation finished. You can now use /stratify [industry] in your AI agent.');
  process.exit(0);
}

// 2. Skill Auto-Uninstaller for AI Agent environments
if (args.includes('--uninstall-skill') || args.includes('--remove-skill')) {
  printBanner();
  console.log('[UNINSTALL] Removing STRATIFY Skill from AI Agent directories...\n');

  const homeDir = os.homedir();
  const cwd = process.cwd();
  const targetDirs = [
    path.join(homeDir, '.gemini', 'antigravity', 'skills', 'stratify'),
    path.join(homeDir, '.agent', 'skills', 'stratify'),
    path.join(homeDir, '.cursor', 'skills', 'stratify'),
    path.join(cwd, '.agent', 'skills', 'stratify')
  ];

  let removedCount = 0;
  for (const dir of targetDirs) {
    if (fs.existsSync(dir) && !dir.startsWith(rootDir)) {
      try {
        fs.rmSync(dir, { recursive: true, force: true });
        console.log(`[REMOVED] Deleted skill directory: ${dir}`);
        removedCount++;
      } catch (err) {
        console.log(`[WARNING] Could not delete ${dir}: ${err.message}`);
      }
    }
  }

  // Also remove local project bridge files in CWD if running from another project
  if (cwd !== rootDir) {
    const bridgeFiles = ['GEMINI.md', 'CLAUDE.md', 'AGENTS.md', '.cursorrules'];
    for (const bf of bridgeFiles) {
      const targetFile = path.join(cwd, bf);
      if (fs.existsSync(targetFile)) {
        try {
          const content = fs.readFileSync(targetFile, 'utf8');
          if (content.includes('STRATIFY')) {
            fs.unlinkSync(targetFile);
            console.log(`[REMOVED] Deleted project rule: ${bf}`);
          }
        } catch (e) {}
      }
    }
  }

  if (removedCount === 0) {
    console.log('[INFO] No installed STRATIFY skills found in default agent directories.');
  }

  console.log('\n[COMPLETE] Uninstallation finished. STRATIFY skill has been removed.');
  process.exit(0);
}

// 3. Launch Web Dashboard
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

// 3. License & Intellectual Property Compliance Audit
if (args.includes('--compliance') || args.includes('--licenses')) {
  printBanner();
  const pythonCmd = getPythonCommand();
  if (!pythonCmd) {
    const licFile = path.join(rootDir, 'THIRD_PARTY_LICENSES.md');
    if (fs.existsSync(licFile)) {
      console.log(fs.readFileSync(licFile, 'utf8'));
    } else {
      console.log('[COMPLIANCE] All 21 core skills are independently developed and APPROVED under MIT.');
    }
    process.exit(0);
  }

  const child = spawn(pythonCmd, [path.join(rootDir, 'stratify.py'), '--compliance'], {
    cwd: rootDir,
    stdio: 'inherit'
  });

  child.on('exit', (code) => {
    process.exit(code || 0);
  });
  return;
}

// 4. Run STRATIFY Command via CLI
printBanner();

const pythonCmd = getPythonCommand();
if (!pythonCmd) {
  // Graceful fallback: Run native Node.js research engine when Python is not installed
  const { runNativeCli } = require('./native-orchestrator.js');
  runNativeCli(args);
  return;
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
