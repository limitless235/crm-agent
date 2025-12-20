import requests
import asyncio
import websockets
import json
import time
import pytest
import uuid

API_URL = "http://localhost:8000/api/v1"
WS_URL = "ws://localhost:8000/api/v1"

class TestSystemE2E:
    @pytest.fixture(scope="class")
    def test_user(self):
        email = f"test_{uuid.uuid4().hex[:6]}@example.com"
        password = "testpassword123"
        
        # 1. Register User
        res = requests.post(f"{API_URL}/auth/register", json={
            "email": email,
            "password": password
        })
        assert res.status_code == 200
        
        # 2. Login
        res = requests.post(f"{API_URL}/auth/login", data={
            "username": email,
            "password": password
        })
        assert res.status_code == 200
        token = res.json()["access_token"]
        
        return {"email": email, "token": token}

    def test_ticket_flow(self, test_user):
        token = test_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create Ticket
        ticket_data = {
            "title": "Problem with connection",
            "initial_message": "My internet is very slow, help!"
        }
        res = requests.post(f"{API_URL}/tickets/", json=ticket_data, headers=headers)
        assert res.status_code == 200
        ticket = res.json()
        ticket_id = ticket["id"]
        
        # 2. Check Ticket in List
        res = requests.get(f"{API_URL}/tickets/", headers=headers)
        assert res.status_code == 200
        assert any(t["id"] == ticket_id for t in res.json())

        # 3. Wait for AI response (Worker might take a moment)
        # We poll for messages on this ticket
        max_retries = 10
        ai_responded = False
        for _ in range(max_retries):
            res = requests.get(f"{API_URL}/tickets/{ticket_id}/messages", headers=headers)
            assert res.status_code == 200
            messages = res.json()
            # If there's more than 1 message, AI probably responded
            if len(messages) > 1:
                ai_responded = True
                break
            time.sleep(2)
        
        assert ai_responded, "AI worker failed to respond within time limit"

    @pytest.mark.asyncio
    async def test_websocket_notification(self, test_user):
        token = test_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create a new ticket
        ticket_res = requests.post(f"{API_URL}/tickets/", json={
            "title": "WS Test Ticket",
            "initial_message": "Testing real-time updates"
        }, headers=headers)
        ticket_id = ticket_res.json()["id"]

        # 2. Connect to WS
        # Note: In our current implementation, the WS URL doesn't strictly check the token in the query yet, 
        # but the request path includes ticket_id.
        ws_endpoint = f"{WS_URL}/tickets/ws/{ticket_id}"
        
        async with websockets.connect(ws_endpoint) as websocket:
            # 3. Post another message via API to trigger a broadcast
            # (In our architecture, the worker will publish to Redis after processing)
            # For this test, let's just wait for the worker to process the initial message
            
            try:
                # Wait for message from WS
                done, pending = await asyncio.wait(
                    [websocket.recv()],
                    timeout=15
                )
                
                if done:
                    msg_text = done.pop().result()
                    data = json.loads(msg_text)
                    assert data["type"] == "NEW_MESSAGE"
                    assert data["ticket_id"] == ticket_id
                else:
                    pytest.fail("WebSocket timed out waiting for message")
            finally:
                for task in pending:
                    task.cancel()

if __name__ == "__main__":
    # This allows running the script directly if not using pytest
    print("Run with: pytest tests/e2e/test_system.py")
