import json
import boto3
from openai import OpenAI


def get_ssm_parameter(parameter_name):
    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except Exception as e:
        print(f"Error retrieving parameter {parameter_name} from SSM: {e}")
        raise


def get_all_items():
    try:
        response = table.scan()
        items = [item["word"] for item in response.get("Items", [])]
        formatted_items = ", ".join(items)
        return formatted_items
    except Exception as e:
        print(f"Error retrieving items from DynamoDB: {e}")
        raise


def put_items_in_db_table(items):
    try:
        with table.batch_writer() as batch:
            for item_entry in items:
                if not all(
                    key in item_entry for key in ("item", "explanation", "example")
                ):
                    raise ValueError(
                        f"Invalid entry: {item_entry}. Must contain 'item', 'explanation', and 'example' keys."
                    )
                batch.put_item(
                    Item={
                        "word": item_entry["item"],
                        "explanation": item_entry["explanation"],
                        "example": item_entry["example"],
                    }
                )
        print("All items successfully inserted into the db table.")
    except Exception as e:
        print(f"Error inserting items into the DynamoDB table: {e}")
        raise


def create_prompt(existing_items):
    return (
        "Provide exactly 3 Python items from the Python Standard Library modules or built-in functions,"
        f"but none of those: {existing_items}. "
        "Return them as an array of dictionaries. Each dictionary should include the fields: "
        '"item" (the Python item), "explanation" (a short explanation of the item), '
        'and "example" (a code snippet showing how to use the item). Example format: '
        '[{"item": "item1", "explanation": "explanation1", "example": "example1"}, '
        '[{"item": "item2", "explanation": "explanation2", "example": "example2"}, '
        '[{"item": "item3", "explanation": "explanation3", "example": "example3"}, '
        "Do not add any additional items, explanations, or introductions in your reply. Just return the array."
    )


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("WordsTable")
ssm_client = boto3.client("ssm")
ses_client = boto3.client("ses")
ses_email = get_ssm_parameter("EMAIL_FOR_SES")
client = OpenAI(api_key=get_ssm_parameter("OPEN_AI_API_KEY"))


def lambda_handler(event, context):
    try:
        items = get_all_items()
        prompt = create_prompt(items)

        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )

        response_content = response.choices[0].message.content
        json_response = json.loads(r"{}".format(response_content))

        # Format email for SES
        formatted_html = "<html><body>"
        formatted_html += "<h2>Python Standard Library Examples</h2>"
        formatted_html += (
            "<table border='1' cellpadding='10' style='border-collapse: collapse;'>"
        )
        formatted_html += "<tr><th>Item</th><th>Explanation</th><th>Example</th></tr>"

        for item in json_response:
            formatted_html += f"<tr><td>{item['item']}</td><td>{item['explanation']}</td><td><pre>{item['example']}</pre></td></tr>"

        formatted_html += "</table>"
        formatted_html += "</body></html>"

        ses_client.send_email(
            Source=ses_email,
            Destination={"ToAddresses": [ses_email]},
            Message={
                "Subject": {"Data": "Python Standard Library Examples"},
                "Body": {"Html": {"Data": formatted_html}},
            },
        )

        put_items_in_db_table(json_response)

        return {"statusCode": 200, "body": "Email sent successfully."}

    except Exception as e:
        print(f"Error during execution: {e}")
        return {"statusCode": 500, "body": str(e)}
