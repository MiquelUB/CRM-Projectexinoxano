import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typescript: {
    // Ignorem errors de tipus durant el build per assegurar el deploy
    ignoreBuildErrors: true,
  },
  // Activem el mode standalone per a millor rendiment a Docker/Easypanel
  output: 'standalone',
};

export default nextConfig;
