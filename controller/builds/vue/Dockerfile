FROM node:14-alpine 
# AS build-stage

ARG CURRENT_UID
RUN test -n "$CURRENT_UID"
ARG CURRENT_GID
RUN test -n "$CURRENT_GID"

ARG VUE_APP_NAME
RUN test -n "$VUE_APP_NAME"

ENV VUE_VERSION 15.0.4

#ENV NODE_PATH /opt/node_modules


WORKDIR /app

COPY app/package.json .

RUN yarn install

RUN apk add git bash 

COPY ./app .

# RUN yarn build 

# RUN npm run serve

# production stage
#FROM nginx AS production-stage
#COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY ./docker-entrypoint.sh /entrypoint.sh

RUN   chmod +x /entrypoint.sh

# CMD ["docker-entrypoint"]

COPY banner.sh print_versions.sh /etc/

RUN echo '/bin/bash /etc/banner.sh' >> /etc/bash.bashrc

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]

# CMD ["/entrypoint.sh"]
#CMD ["tail","-f","/dev/null"]
#CMD ["npm","run","serve"]
#CMD ["nginx", "-g", "daemon off;"]