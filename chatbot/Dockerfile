# Use Node 18 Alpine for better stability
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Set NODE_ENV to development for the build process
ENV NODE_ENV=development

# Use npm ci for a clean, reproducible install
RUN npm ci

# Copy all source files
COPY . .

# Build the application with error handling
RUN npm run build || (echo "Build failed!" && exit 1)

# After successful build, switch to production mode
ENV NODE_ENV=production

# Install serve globally for serving static files
RUN npm install -g serve

# Expose the port serve will use
EXPOSE 5173

# Serve the built app using serve
CMD ["serve", "-s", "dist", "-l", "5173"]
