FROM alpine:latest
RUN apk add --no-cache bash python3 git jq make coreutils findutils procps perl
RUN adduser -D -u 1000 tester
USER tester
WORKDIR /workspace
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["sh"]
