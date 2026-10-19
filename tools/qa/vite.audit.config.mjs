// game + tools/qa/model-audit.html in one static build (Mac GPU audit without a dev server): npx vite build --config tools/qa/vite.audit.config.mjs --outDir <dir>
import { defineConfig } from 'vite';
import { resolve } from 'node:path';
const R = resolve(new URL(".", import.meta.url).pathname, "../..");
export default defineConfig({ root: R, base: './', build: { target: 'es2022', rollupOptions: { input: { main: resolve(R, 'index.html'), audit: resolve(R, 'tools/qa/model-audit.html') } } }, define: { __BUILD__: JSON.stringify('v9-' + process.env.SHA) } });
