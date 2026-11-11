import base64
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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


def is_text_safe(text: str) -> bool:
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = response.results[0]

    return not result.flagged


def moderate_form(form, changed_only=False):
    for field in ("image", "title", "description", "text"):

        if field not in form.fields:
            continue

        if changed_only and field not in form.changed_data:
            continue

        value = form.cleaned_data.get(field)

        if value is None or value == "":
            continue

        if field == "image":
            is_safe = is_image_safe(value)
        else:
            is_safe = is_text_safe(value)

        if not is_safe:
            form.add_error(
                field,
                f"This {field} is not allowed."
            )

    return not form.errors