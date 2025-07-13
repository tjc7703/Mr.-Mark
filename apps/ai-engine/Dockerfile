FROM node:20 AS check
WORKDIR /app
RUN apt-get update && apt-get install -y curl \
  && curl -I https://registry.npmjs.org || (echo "NPM 서버 장애" && exit 1)

FROM node:20 AS deps
WORKDIR /app
COPY pnpm-lock.yaml .
RUN corepack enable && corepack prepare pnpm@latest --activate \
  && pnpm config set registry https://registry.npmmirror.com \
  && pnpm install --frozen-lockfile

FROM node:20 AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN pnpm build

FROM node:20 AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
