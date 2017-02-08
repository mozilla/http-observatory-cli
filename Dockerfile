##
# NAME             : fgribreau/httpobs-cli
# VERSION          : latest
# DOCKER-VERSION   : 1.5
# DESCRIPTION      :
# TO_BUILD         : docker build --pull=true --no-cache -t fgribreau/httpobs-cli .
# TO_SHIP          : docker push fgribreau/httpobs-cli
# TO_RUN           : docker run -d fgribreau/httpobs-cli
##

FROM python:3-slim

RUN pip install httpobs-cli

ENTRYPOINT [ "httpobs-cli" ]
