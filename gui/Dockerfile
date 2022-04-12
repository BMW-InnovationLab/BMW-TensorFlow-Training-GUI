# BMW TerchOffice Munich
### STAGE 1: Build ###

# We label our stage as 'builder'
FROM node:12-alpine as builder


COPY package.json ./

RUN npm set progress=false && npm config set depth 0 && npm cache clean --force

## Storing node modules on a separate layer will prevent unnecessary npm installs at each build
RUN npm i  && mkdir /ng-app && cp -R ./node_modules ./ng-app

WORKDIR /ng-app

COPY . .

##recieve the environment name as argument
# ARG ENV_NAME

## Build the angular app in production mode and store the artifacts in dist folder
RUN $(npm bin)/ng build --prod --build-optimizer

# RUN npm install -g @angular/cli@7.3.9
# 
# CMD ng serve --host 0.0.0.0 


### STAGE 2: Setup ###

FROM nginx:1.13.3-alpine

# Copy our default nginx config
COPY nginx/default.conf /etc/nginx/conf.d/

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# From 'builder' stage copy over the artifacts in dist folder to default nginx public folder
COPY --from=builder /ng-app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
