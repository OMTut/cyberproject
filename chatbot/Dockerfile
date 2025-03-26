# Use an official Node.js image
FROM node

# Set the working directory
WORKDIR /chatbot

# Install dependencies
COPY package.json ./

RUN rm -rf node_modules && \
    npm cache clean --force && \
    npm install -g npm@latest && \
    npm i esbuild@0.25.1 && \
    npm i && \
    npm list esbuild && \
    echo "Node version: $(node -v)" && \
    echo "NPM version: $(npm -v)"

# Copy the rest of the app's source code
COPY . .

# Expose the port serve will use
EXPOSE 5173

# Serve the built app
CMD ["npm", "run", "dev"]