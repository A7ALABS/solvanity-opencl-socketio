This repository was made using [SolVanityCL](https://github.com/WincerChan/SolVanityCL), credit for all the original work goes to `SolVanityCL`. This project uses `SolVanityCL` to generate the address and only acts as a wrapper around it to create a pubsub system.

This repository is made to reproduce an issue on linux operating systems when used with google pub/sub package.

## Attribution
Original project: [SolVanityCL](https://github.com/WincerChan/SolVanityCL)
Original Author's name: [WincerChan](https://github.com/WincerChan)
Original License: Refer to LICENSE.SolVanityCL file

## Installation
Requires Python 3.6 or higher.

create a virtual environment

```
python3 -m venv venv
```

Activate the virtual environment
```
source venv/bin/activate
```

Now that all the packages are installed, you can either run the socketio server or the pubsub based server

#### FAST API SERVER

Run the fastapi-socketio server
```
python3 socketapp.py
```
Once the fast api server is up and running, you can connect with a postman socket-io request.


#### GOOGLE PUB/SUB BASED SERVER

Run the google pubsub based server
```
python3 pubsub.py
```
Once the pubsub based server is running, you can publish to `generate` topic using the `publisher.py` script
```
python3 publisher.py
```

Running the publisher will send the generation payload via the `generate` topic while also listening to `on_generate` and `on_error` topic.

