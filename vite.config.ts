import { defineConfig } from 'vite';
import { execSync } from 'node:child_process';
const sha = (() => { try { return execSync('git rev-parse --short HEAD').toString().trim(); } catch { return 'dev'; } })();
export default defineConfig({ base: './', build: { target: 'es2022' }, server: { port: 4173, strictPort: true }, define: { __BUILD__: JSON.stringify(sha) } });
