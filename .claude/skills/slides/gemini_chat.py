#!/usr/bin/env python3
"""
gemini_chat.py — Send a prompt to Gemini via MQTT proxy and get the response.

Uses the subscribe-before-publish pattern with mosquitto CLI tools.
Based on claude-browser-proxy extension API (Soul-Brews-Studio/claude-browser-proxy).

Requires: mosquitto-clients installed, broker on localhost:1883, chrome extension connected.

Usage:
    python gemini_chat.py "Your prompt here"
    python gemini_chat.py --check          # check if Gemini is online
    python gemini_chat.py --timeout 60 "prompt"

Exit codes:
    0 = success (response printed to stdout)
    1 = Gemini offline / extension not connected
    2 = timeout waiting for response
    3 = error
"""

import subprocess
import json
import sys
import time
import argparse


MQTT_HOST = "localhost"
MQTT_PORT = "1883"
TOPIC_CMD = "claude/browser/command"
TOPIC_RES = "claude/browser/response"
TOPIC_ANS = "claude/browser/answer"
TOPIC_STATUS = "claude/browser/status"

# Auto-detect mosquitto CLI path (Windows: C:\Program Files\mosquitto\)
import shutil
import os

def _find_mosquitto_cmd(name):
    """Find mosquitto command, checking PATH first then common install locations."""
    found = shutil.which(name)
    if found:
        return found
    # Windows default install paths
    for d in [r"C:\Program Files\mosquitto", r"C:\Program Files (x86)\mosquitto"]:
        p = os.path.join(d, name + ".exe")
        if os.path.isfile(p):
            return p
    return name  # fallback to bare name

MOSQUITTO_PUB = _find_mosquitto_cmd("mosquitto_pub")
MOSQUITTO_SUB = _find_mosquitto_cmd("mosquitto_sub")


def mqtt_pub(topic, message):
    """Publish a message to MQTT topic."""
    subprocess.run(
        [MOSQUITTO_PUB, "-h", MQTT_HOST, "-p", MQTT_PORT, "-t", topic, "-m", message],
        capture_output=True, text=True, timeout=5
    )


def mqtt_sub_one(topic, wait_sec=5):
    """Subscribe and get one message, with timeout."""
    try:
        result = subprocess.run(
            [MOSQUITTO_SUB, "-h", MQTT_HOST, "-p", MQTT_PORT,
             "-t", topic, "-C", "1", "-W", str(wait_sec)],
            capture_output=True, text=True, timeout=wait_sec + 3
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def send_and_receive(action, params=None, wait_sec=8):
    """Subscribe-before-publish pattern: subscribe first, then publish, read response."""
    msg_id = f"{action}_{int(time.time() * 1000)}"
    payload = {"id": msg_id, "action": action}
    if params:
        payload.update(params)

    # 1. Start subscriber FIRST (in background)
    sub_proc = subprocess.Popen(
        [MOSQUITTO_SUB, "-h", MQTT_HOST, "-p", MQTT_PORT,
         "-t", TOPIC_RES, "-C", "1", "-W", str(wait_sec)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # 2. Small delay for subscription to be ready
    time.sleep(0.3)

    # 3. Publish command
    mqtt_pub(TOPIC_CMD, json.dumps(payload))

    # 4. Read response
    try:
        stdout, _ = sub_proc.communicate(timeout=wait_sec + 3)
        if stdout.strip():
            return json.loads(stdout.strip())
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        sub_proc.kill()
    return None


def check_online():
    """Check if Gemini proxy extension is online via retained status message."""
    raw = mqtt_sub_one(TOPIC_STATUS, wait_sec=3)
    if raw:
        try:
            status = json.loads(raw)
            return status.get("online", False) or status.get("status") == "online"
        except json.JSONDecodeError:
            return "online" in raw.lower()
    return False


def find_gemini_tab():
    """List tabs and find a Gemini tab."""
    resp = send_and_receive("list_tabs", wait_sec=5)
    if resp and "tabs" in resp:
        for tab in resp["tabs"]:
            tab_url = tab.get("url", "")
            tab_title = tab.get("title", "")
            if "gemini" in tab_url.lower() or "gemini" in tab_title.lower():
                return tab.get("id") or tab.get("tabId")
    return None


def wait_for_gemini(tab_id, timeout_ms=60000):
    """Use the extension's built-in wait_response action.

    This tells the extension to wait until Gemini finishes generating,
    then returns. Much more reliable than manual polling.
    """
    wait_sec = max(timeout_ms // 1000 + 5, 20)
    resp = send_and_receive(
        "wait_response",
        {"tabId": tab_id, "timeout": timeout_ms},
        wait_sec=wait_sec
    )
    return resp


def get_gemini_response(tab_id=None):
    """Get Gemini's latest response text using get_response action."""
    params = {}
    if tab_id:
        params["tabId"] = tab_id
    resp = send_and_receive("get_response", params, wait_sec=8)
    if resp:
        # Response may have the answer in different fields
        return resp.get("answer") or resp.get("text") or resp.get("response") or resp.get("content", "")
    return None


def main():
    parser = argparse.ArgumentParser(description="Chat with Gemini via MQTT proxy")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to Gemini")
    parser.add_argument("--check", action="store_true", help="Check if Gemini is online")
    parser.add_argument("--timeout", type=int, default=60, help="Max wait for response (seconds)")
    parser.add_argument("--tab-id", type=int, help="Specific tab ID to use")
    args = parser.parse_args()

    # --- Check mode ---
    if args.check:
        online = check_online()
        if online:
            tab_id = find_gemini_tab()
            if tab_id:
                print(json.dumps({"online": True, "tabId": tab_id}))
            else:
                print(json.dumps({"online": True, "tabId": None, "note": "no gemini tab found"}))
        else:
            print(json.dumps({"online": False}))
        sys.exit(0 if online else 1)

    # --- Chat mode ---
    if not args.prompt:
        print("Error: prompt required", file=sys.stderr)
        sys.exit(3)

    # Step 1: Check online
    if not check_online():
        print("OFFLINE", file=sys.stderr)
        sys.exit(1)

    # Step 2: Find or use tab
    tab_id = args.tab_id
    if not tab_id:
        tab_id = find_gemini_tab()

    if not tab_id:
        # Create a new Gemini tab
        print("No Gemini tab found, creating one...", file=sys.stderr)
        resp = send_and_receive("create_tab", wait_sec=8)
        if resp and resp.get("tabId"):
            tab_id = resp["tabId"]
            print(f"Created tab {tab_id}, waiting for load...", file=sys.stderr)
            time.sleep(5)  # Wait for Gemini page to fully load
        else:
            print("ERROR: could not create Gemini tab", file=sys.stderr)
            sys.exit(3)

    print(f"Using tab {tab_id}", file=sys.stderr)

    # Step 3: Send chat message
    resp = send_and_receive("chat", {"tabId": tab_id, "text": args.prompt}, wait_sec=8)
    if not resp or resp.get("success") is False:
        print("ERROR: failed to send chat message", file=sys.stderr)
        sys.exit(3)

    print("Prompt sent, waiting for Gemini to respond...", file=sys.stderr)

    # Step 4: Wait for Gemini to finish generating (built-in extension action)
    timeout_ms = args.timeout * 1000
    wait_result = wait_for_gemini(tab_id, timeout_ms=timeout_ms)

    if wait_result and wait_result.get("timeout"):
        print("TIMEOUT: Gemini did not finish in time", file=sys.stderr)
        # Still try to get partial response
        text = get_gemini_response(tab_id)
        if text:
            print(text)
            sys.exit(0)
        sys.exit(2)

    # Step 5: Get the response text
    text = get_gemini_response(tab_id)

    if text:
        print(text)
        sys.exit(0)
    else:
        # Fallback: try listening on answer topic
        print("Trying answer topic fallback...", file=sys.stderr)
        raw = mqtt_sub_one(TOPIC_ANS, wait_sec=5)
        if raw:
            print(raw)
            sys.exit(0)

        print("ERROR: could not retrieve Gemini response", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
