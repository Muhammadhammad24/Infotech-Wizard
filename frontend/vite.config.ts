import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Replace with your backend URL
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8000', // Replace with your backend URL
        changeOrigin: true,
      },
    },
  },
});