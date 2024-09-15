# Fetching the latest node image on apline linux
FROM node:latest AS builder

# Declaring env
ENV NODE_ENV production

# Setting up the work directory
WORKDIR /app

RUN npm config set https-proxy=http://proxy.esl.cisco.com:80

# Installing dependencies
COPY ./package.json ./
RUN npm install

# Copying all the files in our project
COPY . ./

# Building our application
RUN npm run build

# Fetching the latest nginx image
FROM nginx:latest

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# COPY ../certs/ssl-bundle.crt /etc/nginx/ssl/ssl-bundle.crt
# COPY ../certs/dcaf.key /etc/nginx/ssl/dcaf.key

# Copying built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html