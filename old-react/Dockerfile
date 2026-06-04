# ─── Stage 1: Build ────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Install bun (karena proyek menggunakan bun.lock)
RUN npm install -g bun

# Copy manifest & lockfile dulu (layer caching)
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy seluruh source
COPY . .

# Build production bundle
RUN bun run build

# ─── Stage 2: Serve ────────────────────────────────────────────────────────────
FROM nginx:1.27-alpine AS runner

# Hapus default config nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/app.conf

# Copy hasil build dari stage sebelumnya
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
