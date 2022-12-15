FROM node:18-alpine

ENV NODE_ENV=production

WORKDIR /app/

ADD package.json yarn.lock /app/
RUN yarn install

ADD . /app/

CMD ["node", "server.js"]
