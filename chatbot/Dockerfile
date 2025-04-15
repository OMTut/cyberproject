# Use lightweight Node image for serving static files
FROM node:alpine

# Set the working directory
WORKDIR /app

# Install serve globally for serving static files
RUN npm install -g serve

# Copy only the built files (assuming app is pre-built locally)
COPY ./dist ./dist

# Expose the port serve will use
EXPOSE 5173

# Serve the built app using serve
CMD ["serve", "-s", "dist", "-l", "5173"]
