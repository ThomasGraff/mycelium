# Step 1: Build the frontend app
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .
RUN yarn build

# Step 2: Serve the frontend using Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
