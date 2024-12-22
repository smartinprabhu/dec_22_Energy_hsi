import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import reactRefresh from "@vitejs/plugin-react-refresh";
import replace from '@rollup/plugin-replace';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), reactRefresh()],
  base: "/",
  server: {
    host: true,
    port: 3008,
  },
  build: {
    rollupOptions: {
      plugins: [
        replace({
          'import.meta.env.VITE_API_URL': process.env.REACT_APP_API_URL,
        }),
      ],
    },
  },
});
