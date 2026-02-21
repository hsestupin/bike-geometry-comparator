import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {fileURLToPath} from 'node:url';

const src = fileURLToPath(new URL('./src', import.meta.url));

// https://vitejs.dev/config/
export default defineConfig({
  base: '/bike-geometry-comparator/',
  plugins: [react()],
  resolve: {
    alias: {
      '@': src,
    },
  },
});
