FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

ARG ACIE_API_BASE=/api
ARG WEBPACK_PUBLIC_PATH=/
ENV ACIE_API_BASE=$ACIE_API_BASE
ENV WEBPACK_PUBLIC_PATH=$WEBPACK_PUBLIC_PATH

RUN npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
