import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://serene-nature-production-7818.up.railway.app',
        changeOrigin: true,
      },
    },
  },
})
