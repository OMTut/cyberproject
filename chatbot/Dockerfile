# Use Node 22.9.0 to match local environment exactly
FROM node:22.9.0

# Set the working directory
WORKDIR /chatbot

# Install dependencies
COPY package.json ./

# Clean installation with platform-specific flags
RUN npm cache clean --force && \
    npm install --platform=linux --arch=x64 && \
    echo "Node version: $(node -v)" && \
    echo "NPM version: $(npm -v)" && \
    echo "esbuild version: $(npm list esbuild | grep esbuild)"

# Copy the rest of the app's source code
COPY . .

# Expose the port serve will use
EXPOSE 5173

# Serve the built app
CMD ["npm", "run", "dev"]