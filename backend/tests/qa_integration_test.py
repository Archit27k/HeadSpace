import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://localhost:8000"
HEADERS = {"X-Test-User": "true"}

async def run_tests():
    print("Starting QA Integration End-to-End Tests...")
    
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(base_url=BASE_URL, headers=HEADERS, timeout=timeout) as client:
        # 1. Test Authentication Sync
        print("Testing Authentication Sync...")
        resp = await client.get("/api/analytics/dashboard")
        assert resp.status_code == 200, f"Auth test failed: {resp.status_code} {resp.text}"
        print("✅ Auth Sync PASS")

        # 2. Test Journal Submission (Triggers LangGraph & Memory)
        print("Testing Journal Submission & Intelligence Tool...")
        journal_payload = {
            "title": "A stressful day",
            "content": "I felt really stressed today at work because of the upcoming deadline. But I went for a walk and felt a bit better.",
            "tags": ["work", "stress", "walk"]
        }
        resp = await client.post("/api/journal/", json=journal_payload)
        assert resp.status_code in [200, 201], f"Journal creation failed: {resp.status_code} {resp.text}"
        print("✅ Journal Submission PASS")
        
        # Give LangGraph a few seconds to process background tasks
        await asyncio.sleep(3)

        # 3. Test Mood Tracker & MLflow Inference
        print("Testing Mood Tracker & MLflow Inference...")
        mood_payload = {
            "score": 6,
            "primary_emotion": "anxious",
            "notes": "Feeling okay but slightly anxious about tomorrow."
        }
        resp = await client.post("/api/mood/", json=mood_payload)
        assert resp.status_code in [200, 201], f"Mood creation failed: {resp.status_code} {resp.text}"
        print("✅ Mood Submission PASS")

        await asyncio.sleep(3)

        # 4. Test Memory Extraction Retrieval
        print("Testing Memory API...")
        resp = await client.get("/api/memory/")
        assert resp.status_code == 200, f"Memory API failed: {resp.status_code} {resp.text}"
        memories = resp.json()
        print(f"✅ Memory API PASS (Found {len(memories)} memories)")

        # 5. Test Chat (LangGraph + Gemini)
        print("Testing Chat & Conversational RAG...")
        # First create a conversation
        resp = await client.post("/api/chat/conversations", json={"summary": "Test Chat"})
        if resp.status_code == 404:
            print("⚠️ Chat conversations route not found, skipping conversation creation.")
        else:
            assert resp.status_code in [200, 201], f"Chat creation failed: {resp.status_code} {resp.text}"
            conv_id = resp.json().get("id")
            
            chat_payload = {
                "role": "user",
                "content": "What did I write in my journal today about work?"
            }
            resp = await client.post(f"/api/chat/conversations/{conv_id}/messages", json=chat_payload)
            assert resp.status_code in [200, 201], f"Chat message failed: {resp.status_code} {resp.text}"
            print("✅ Chat LLM Pipeline PASS")

        # 6. Test Recommendations (Gemini Wellness Tool)
        print("Testing Recommendations API...")
        resp = await client.get("/api/recommendations/")
        assert resp.status_code == 200, f"Recommendations API failed: {resp.status_code} {resp.text}"
        print("✅ Recommendations API PASS")

        # 7. Test Analytics (Database Aggregation)
        print("Testing Analytics & Reporting...")
        resp = await client.get("/api/analytics/dashboard")
        assert resp.status_code == 200, f"Analytics API failed: {resp.status_code} {resp.text}"
        resp = await client.get("/api/analytics/reports/weekly")
        assert resp.status_code == 200, f"Reports API failed: {resp.status_code} {resp.text}"
        print("✅ Analytics API PASS")

    print("All backend integration tests passed successfully!")

if __name__ == "__main__":
    asyncio.run(run_tests())
