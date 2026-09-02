import base64
from openai import OpenAI

client = OpenAI()

def is_image_safe(image):
    encoded = base64.b64encode(image.read()).decode("utf-8")

    data_url = f"data:{image.content_type};base64,{encoded}"

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url,
                },
            }
        ],
    )

    image.seek(0)
    result = response.results[0]
    print("FLAGGED:", result.flagged)
    print("SEXUAL:", result.category_scores.sexual)
    sexual_score = result.category_scores.sexual

    if result.flagged or sexual_score > 0.2:
        return False

    return True