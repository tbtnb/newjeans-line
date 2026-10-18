import { defineConfig } from 'vite';
// Separate page published at gh-pages /tapper/ (audio comes from the live site's ../audio/)
export default defineConfig({ root: 'tapper', base: './', publicDir: false, build: { target: 'es2020', outDir: '/workspace/nj-tapper-dist', emptyOutDir: true } });
