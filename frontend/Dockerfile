FROM node:15.3.0-alpine3.10
WORKDIR /app
COPY package.json /app/package.json
RUN apk add bash vim
RUN npm install
RUN npm install @vue/cli@4.3.1 -g
CMD ["npm", "run", "serve"]
