"""
Smoke Test — run this before starting any exercise.
Expected output:  ✅  API connection OK — model replied: READY

Troubleshooting:
  "NEBIUS_KEY not set"   → open .env and paste your key (no quotes)
  "Connection refused"   → check your internet connection
  "401 Unauthorized"     → your API key is wrong or expired
  "ModuleNotFoundError"  → run `uv sync` first

Model note (2026-04-13):
  This uses Llama-3.3-70B-Instruct (the Base variant, not `_fast`).
  Only the `_fast` variant was removed in the Nebius deprecation round;
  the Base variant is still actively supported. If you see connection
  errors mentioning the model string, confirm you have pulled the latest
  main — the earlier scaffold may have referenced the wrong variant.
"""

import os
import sys
import certifi
import httpx
from openai import OpenAI
from dotenv import load_dotenv

import ssl

def _build_ssl_context() -> ssl.SSLContext:
    """Return an SSL context that trusts certifi's CA bundle plus any cert
    pointed to by the SSL_CERT_FILE environment variable (e.g. a corporate
    proxy / Zscaler certificate).

    Python 3.12+ enables ssl.VERIFY_X509_STRICT by default, which rejects CA
    certificates whose Basic Constraints extension is present but not marked
    critical (a common trait of corporate proxy certs such as Zscaler).
    We clear that flag so the SDK can reach the API through the proxy.
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    extra_cert = os.environ.get("SSL_CERT_FILE")
    if extra_cert:
        ctx.load_verify_locations(extra_cert)
    # VERIFY_X509_STRICT was added in Python 3.10 and turned on by default in
    # 3.12.  Clearing it relaxes the RFC 5280 requirement that a CA cert's
    # Basic Constraints extension must be marked critical — required for some
    # corporate-issued CA certs (e.g. Zscaler) to be accepted.
    if hasattr(ssl, "VERIFY_X509_STRICT"):
        ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return ctx

load_dotenv()

key = os.getenv("NEBIUS_KEY", "")
if not key or key == "sk-your-key-here":
    print("❌  NEBIUS_KEY not set. Copy .env.example → .env and paste your key.")
    sys.exit(1)

print("Connecting to Nebius API...")

try:
    transport_client = httpx.Client(verify=_build_ssl_context())
    client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=key,
        http_client=transport_client,
    )
    resp = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": "Reply with exactly one word: READY"}],
        max_tokens=10,
        temperature=0,
    )
    answer = resp.choices[0].message.content.strip()
    if "READY" in answer.upper():
        print(f"✅  API connection OK — model replied: {answer}")
        print(f"    Model : meta-llama/Llama-3.3-70B-Instruct  (Base variant)")
        print(f"    Tokens: {resp.usage.total_tokens}")
        print("\nYou're ready. Start with:")
        print("    uv run python week1/exercise1_context.py")
    else:
        print(f"⚠️   Unexpected reply: '{answer}'")
        print("    Connection works but model behaved unexpectedly. Try again.")
except Exception as e:
    print(f"❌  Connection failed: {e} ({type(e).__name__})")
    if getattr(e, "__cause__", None):
        print(f"    Cause: {e.__cause__} ({type(e.__cause__).__name__})")
    sys.exit(1)
finally:
    if "transport_client" in locals():
        transport_client.close()
