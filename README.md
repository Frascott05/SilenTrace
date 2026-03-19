# SilentTrace

Before starting the container, we suggest you to move all the dumps you wanna analyze
in the dumps folder.

You can still do that later on since the volumes ar addedd to the container or using docker cp

# Advises
We advise you to not deploy the application on an open web server, since it's made
for local server/pc use. Despite the JWT authentication it's not designed for going on the internet

Change the secret on the .env file and DON'T EXPOSE IT

# USAGE
You can Build the image with the following command:
`docker compose build`

Then you can deploy the container with the following command (the --service-ports is used for exposing the port)
`docker compose run --service-ports silentrace`

If you want to change some configurations on the ports, or you want to add some API keys you can modify the .env file