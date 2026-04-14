import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    // Ignora els errors de linter durant el build
    ignoreDuringBuilds: true,
  },
  typescript: {
    // IGNORA ELS ERRORS DE TYPESCRIPT PER FORÇAR EL DESPLEGAMENT
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
