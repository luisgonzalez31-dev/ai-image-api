import base64
import json
from openai import OpenAI

client = OpenAI()

async def analyze_image(file):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
    Analiza la imagen y responde SOLO en formato JSON válido con esta estructura:

    {
      "objects": ["lista de objetos principales"],
      "activity": "qué está ocurriendo",
      "context": "dónde ocurre la escena",
      "confidence": "alta, media o baja"
    }

    No expliques nada, solo devuelve JSON válido.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }]
    )

    try:
        result_text = response.output[0].content[0].text

        # LIMPIEZA DE MARKDOWN
        if "```" in result_text:
            result_text = result_text.replace("```json", "").replace("```", "").strip()

        result_json = json.loads(result_text)

        return result_json

    except Exception as e:
        return {
            "error": "No se pudo parsear la respuesta",
            "detalle": str(e),
            "raw_response": result_text
        }