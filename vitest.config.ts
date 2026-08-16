import { defineConfig } from "vitest/config";
import { resolve } from "path";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    css: false,
  },
  resolve: {
    alias: {
      "@prep/schemas": resolve(__dirname, "./packages/schemas/exercises.ts"),
      "@": resolve(__dirname, "./src"),
    },
  },
});
