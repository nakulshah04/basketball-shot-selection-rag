export function connectWebSocket(
  onMessage: (data: any) => void
) {
  const ws = new WebSocket("ws://127.0.0.1:8000/ws/realtime");

  ws.onopen = () => {
    console.log("WebSocket connected");
  };

  ws.onmessage = (event) => {
    onMessage(JSON.parse(event.data));
  };

  ws.onerror = (err) => {
    console.error("WebSocket error", err);
  };

  return ws;
}