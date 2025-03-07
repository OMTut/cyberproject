# Use an official Node.js image
FROM node

# Set the working directory
WORKDIR /dashboard

# Install dependencies
COPY package.json ./
RUN npm i

# Copy the rest of the app's source code
COPY . .

# Expose the port serve will use
EXPOSE 5174

# Serve the built app
CMD ["npm", "run", "dev"]