
APP="flask"
# set a version
VERSION=${git rev-parse HEAD | cut -c 1-10}
salt-call event.send "app/deploy" "{'app':'${APP}','version':'${VERSION}'}"
