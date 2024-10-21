# Step 1: Build the frontend app
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .
RUN yarn build

# Step 2: Serve the frontend using Nginx
FROM nginx:alpine

# Copy the built app
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the Nginx configuration template
COPY config/nginx.conf /etc/nginx/nginx.conf.template

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

# Set environment variable with a default value
ENV BACKEND_URL=http://0.0.0.0:8000

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
