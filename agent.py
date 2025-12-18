# agent.py

import json
from groq import Groq
from mcp_client import invoke_tool

client = Groq()

SYSTEM_PROMPT = """
You are a customer support assistant for an electronics store.
You have access to backend tools via JSON-RPC.

When you need to call a tool, respond ONLY in this JSON format:

{
  "tool": "<tool_name>",
  "arguments": { ... }
}

Otherwise, respond normally to the user.
"""


def run_agent(user_message: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0
    )

    reply = completion.choices[0].message.content

    # Try to parse tool call
    try:
        data = json.loads(reply)
        if "tool" in data:
            tool_name = data["tool"]
            args = data.get("arguments", {})

            tool_result = invoke_tool(tool_name, args)

            # Send tool result back to LLM for final answer
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "tool", "content": tool_result})

            final = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0
            )

            return final.choices[0].message["content"]

    except Exception:
        pass

    # Normal response
    return reply