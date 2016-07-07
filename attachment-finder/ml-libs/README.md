
##Run the ML-LIBS scripts

```
export GOOGLE_API_KEY=<key>
python test.py
```

Output should look like:

```
[...]
FINAL SCORE IS 0.970114942529. MAX is 1. MIN is 0.
```

##Dockerized server

Build the server image:

```
docker build -t attachment-finder .
```

Run with port 5000 mapped, connect at <container_addr>:5000

```
docker run -d -p 80:5000 -e GOOGLE_API_KEY=XXX attachment-finder
```
