import os
import json
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def parse_query(user_query):

    prompt = f"""
You are a shopping query understanding system.

Analyze the following user request and return ONLY valid JSON.

User request:
"{user_query}"

Return exactly this structure:

{{
    "request_type": "discovery",
    "query": "",
    "max_budget": null,
    "max_delivery_days": null,
    "excluded_brands": []
}}

Rules:

1. request_type must be exactly one of:
   "discovery", "reorder", "mixed".

2. Use "discovery" when the user wants to
   find or discover products.

3. Use "reorder" when the user wants products
   they have previously purchased.

4. Use "mixed" when the user wants both:
   previously purchased products and new products.

5. query should contain the semantic product intent
   for product discovery.

6. For a pure reorder request, query can be an empty string.

7. max_budget should be a number if the user
   specifies a maximum price.

8. max_delivery_days should be a number if the user
   specifies a maximum delivery time.

9. excluded_brands should contain brands that
   the user explicitly does not want.

10. Use null when budget or delivery time
    is not specified.

11. Use an empty list when there are no
    excluded brands.

12. Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    parsed = json.loads(content)

    return parsed


if __name__ == "__main__":

    test_queries = [
        "I want comfortable shoes for travelling",
        "Reorder my usual products",
        "Reorder my usual products and find comfortable shoes under 500"
    ]

    for query in test_queries:

        print("\n" + "=" * 60)
        print("QUERY:")
        print(query)

        result = parse_query(query)

        print("\nPARSED RESULT:")
        print(result)