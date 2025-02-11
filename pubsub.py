import json
import logging
from src.generator import search_pubkey, get_result
import uvicorn
from google.cloud import pubsub_v1
from google.auth import jwt
import asyncio

logging.basicConfig(level="INFO", format="[%(levelname)s %(asctime)s] %(message)s")
PROJECT_ID="mechaadi"
service_account_info = json.load(open("mechaadi-8404be63607d.json"))

# subscriber authentication
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

# publisher authentication
publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials_pub = credentials.with_claims(audience=publisher_audience)
publisher = pubsub_v1.PublisherClient(credentials=credentials_pub)


generate_topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic='on_generated',
)

error_topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic='on_error', 
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=PROJECT_ID,
    sub='generate-sub',  # Set this to something appropriate.
)


async def generate_address(prefix, jobId,  isCaseSensitive=True):
    starts_with_prefix = prefix
    ends_with_suffix = ""
    num_keys_to_generate = 1
    select_specific_device = False
    iteration_bits_value = 24
    if(len(starts_with_prefix) > 4):
        starts_with_prefix = starts_with_prefix.lower()

    generated_result = search_pubkey(
                starts_with_prefix,
                ends_with_suffix,
                num_keys_to_generate,
                select_specific_device,
                iteration_bits_value,
                isCaseSensitive
            )
    logging.info("Generation finished, making private and public key")
    privateKey, pubKey = get_result(generated_result)
    logging.info("Pub/secret key made, emitting result")
    decoded_message = {"privateKey": privateKey, "pubKey": pubKey}
    
    json_result = json.dumps({"privateKey": decoded_message["privateKey"], "pubKey": decoded_message["pubKey"], "jobId": jobId})
    future = publisher.publish(generate_topic, bytes(json_result, "utf-8"))
    future.result()
    logging.info("Result emitted")
    return 'Generated'


def generate(message):
    data = message.data.decode("utf-8")
    body = json.loads(data)
    prefix = body["prefix"]
    jobId = body["jobId"]
    isCaseSensitive = body["isCaseSensitive"]
    message.ack()
    try:
        logging.info("Generation started")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate_address(prefix, jobId, isCaseSensitive))
        # generate_address(prefix, jobId, isCaseSensitive)
    except Exception as e:
        print(e)
        logging.info("Error while generation, sending error event")
        json_result = json.dumps({"error": str(e), "jobId":jobId})
        future = publisher.publish(error_topic, bytes(json_result, "utf-8"))
        future.result()

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    gpu_devices = []
    future = subscriber.subscribe(subscription_name, generate)
    logging.info("Listening for generate event, generator is live")
    loop.run_forever()

if __name__ == "__main__":
    main()



