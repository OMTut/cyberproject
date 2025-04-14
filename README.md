# Cyberproject

## Docker Install

requirements<BR>
windows
- docker desktop

linux
- docker
- docker-compose


cd into cyberproject director
```yaml
docker-compose up --build
```

or to run it without rebuilding
```yaml
docker-compose up -d
```

if there is a previous container already
```yaml
docker-compose down
```
then compose it up to re-build it

### Ports
The ports are currently mapped to the following
- chatbot 5173
- api 5000

in a browser, goto localhost:port

### Noble Team Members
Sam Arshad, Alyana Imperial, Lucy Ngui, Jason Tuttle, Jonas Tuttle