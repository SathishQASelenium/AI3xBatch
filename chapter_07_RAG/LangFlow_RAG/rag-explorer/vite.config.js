import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const baseUrl = env.VITE_LANGFLOW_BASE_URL || 'http://localhost:7860'
  const flowId = env.VITE_LANGFLOW_FLOW_ID
  const apiKey = env.VITE_LANGFLOW_API_KEY

  return {
    plugins: [react()],
    server: {
      port: 5176,
      open: true,
      proxy: {
        // Browser calls same-origin /api/chat; this rewrites to the real
        // Langflow run endpoint and attaches the secret key server-side so
        // it never appears in browser network calls.
        '/api/chat': {
          target: baseUrl,
          changeOrigin: true,
          rewrite: () => `/api/v1/run/${flowId}?stream=false`,
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq) => {
              if (apiKey) proxyReq.setHeader('x-api-key', apiKey)
              proxyReq.setHeader('Content-Type', 'application/json')
            })
          },
        },
      },
    },
  }
})
