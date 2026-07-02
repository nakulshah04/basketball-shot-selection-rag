import type { StreamPayload } from "../types";

interface WebSocketHandlers {
  onClose?: () => void;
  onError?: (message: string) => void;
  onMessage: (data: StreamPayload) => void;
  onOpen?: () => void;
}

const DEFAULT_WS_URL = "ws://127.0.0.1:8000/ws/realtime";

export function connectWebSocket({
  onClose,
  onError,
  onMessage,
  onOpen,
}: WebSocketHandlers) {
  const wsUrl = import.meta.env.VITE_WS_URL ?? DEFAULT_WS_URL;
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    onOpen?.();
  };

  ws.onmessage = (event) => {
    try {
      onMessage(JSON.parse(event.data) as StreamPayload);
    } catch {
      onError?.("Received an unreadable realtime payload.");
    }
  };

  ws.onerror = () => {
    onError?.("Realtime connection error.");
  };

  ws.onclose = () => {
    onClose?.();
  };

  return ws;
}
