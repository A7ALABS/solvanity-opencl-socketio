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

