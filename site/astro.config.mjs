import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  output: "static",
  integrations: [mdx()],
  site: "https://physics-primitive-agent.github.io",
  base: "/physics-primitive-agent",
});
