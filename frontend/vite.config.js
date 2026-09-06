import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'task-alb-168342689.us-east-1.elb.amazonaws.com'
    ]
  }
})