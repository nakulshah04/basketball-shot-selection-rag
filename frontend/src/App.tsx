import { useEffect, useState } from "react";
import { connectWebSocket } from "./services/websocket";
import type {
  Critique,
  Decision,
  Evidence,
  GameEvent,
  StreamError,
  StreamPayload,
} from "./types";
import EventCard from "./components/EventCard";
import EvidenceCard from "./components/EvidenceCard";
import DecisionCard from "./components/DecisionCard";
import "./App.css";

type ConnectionState = "connecting" | "connected" | "closed" | "error";

function parseJsonPayload<T>(value?: T | string): T | undefined {
  if (!value) return undefined;
  if (typeof value !== "string") return value;
  try {
    return JSON.parse(value) as T;
  } catch {
    return undefined;
  }
}

function App() {
  const [connectionState, setConnectionState] =
    useState<ConnectionState>("connecting");
  const [event, setEvent] = useState<GameEvent>();
  const [decision, setDecision] = useState<Decision>();
  const [critique, setCritique] = useState<Critique>();
  const [streamError, setStreamError] = useState<StreamError>();
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [clientError, setClientError] = useState<string>();

  useEffect(() => {
    const ws = connectWebSocket({
      onClose: () =>
        setConnectionState((current) =>
          current === "error" ? current : "closed",
        ),
      onError: (message) => {
        setConnectionState("error");
        setClientError(message);
      },
      onMessage: (data: StreamPayload) => {
        if (data.status === "connected") {
          setConnectionState("connected");
        }
        if (data.event) setEvent(data.event);
        if (data.error) {
          setStreamError(data.error);
          return;
        }
        setStreamError(undefined);

        const nextDecision = parseJsonPayload<Decision>(data.decision);
        const nextCritique = parseJsonPayload<Critique>(data.critique);

        if (nextDecision) setDecision(nextDecision);
        if (nextCritique) setCritique(nextCritique);
        if (data.evidence) setEvidence(data.evidence);
      },
      onOpen: () => setConnectionState("connected"),
    });

    return () => ws.close();
  }, []);

  return (
    <main className="dashboard">
      <header className="topbar">
        <div>
          <p className="eyebrow">Agentic Shot Selection</p>
          <h1>Make the next possession count.</h1>
        </div>
        <span className={`status ${connectionState}`}>{connectionState}</span>
      </header>

      {(clientError || streamError) && (
        <section className="alert">
          <strong>{streamError?.message ?? clientError}</strong>
          {streamError?.detail && <span>{streamError.detail}</span>}
        </section>
      )}

      <div className="dashboard-grid">
        {event ? (
          <EventCard event={event} />
        ) : (
          <section className="panel">
            <h2>Live Game State</h2>
            <p className="muted">Waiting for realtime events...</p>
          </section>
        )}
        <DecisionCard decision={decision} critique={critique} />
        <EvidenceCard evidence={evidence} />
      </div>
    </main>
  );
}

export default App;
