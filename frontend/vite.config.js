import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'alb-task-1551682951.us-east-1.elb.amazonaws.com'
    ]
  }
})