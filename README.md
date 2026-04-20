curl -X POST http://localhost:8000/run \                               
  -H "Content-Type: application/json" \
  -d '{"memory_file":"Snapshot1.vmem", "plugins":["vadinfo"], "os":"windows","process":4}'


{"job_id":"3784f9da-c407-4683-b8d4-0e6d27efb2b6"}  


curl http://localhost:8000/status/3784f9da-c407-4683-b8d4-0e6d27efb2b6

curl http://localhost:8000/results/3784f9da-c407-4683-b8d4-0e6d27efb2b6



uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
npm run dev -- --host