FROM node:20 AS builder
WORKDIR /app

ARG REACT_APP_API
ENV REACT_APP_API=${REACT_APP_API}

COPY . .
RUN npm install
RUN npm run build

# Stage 2: Serve static files
FROM nginx:stable-alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf