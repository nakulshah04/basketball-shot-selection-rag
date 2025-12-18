import { useEffect, useState } from "react";
import { connectWebSocket } from "./services/websocket";
import type { StreamPayload, GameEvent, Decision, Critique } from "./types";
import EventCard from "./components/EventCard";
import DecisionCard from "./components/DecisionCard";

function App() {
  const [event, setEvent] = useState<GameEvent>();
  const [decision, setDecision] = useState<Decision>();
  const [critique, setCritique] = useState<Critique>();

  useEffect(() => {
    const ws = connectWebSocket((data: StreamPayload) => {
      if (data.event) setEvent(data.event);
      if (typeof data.decision === "string") {
        try { setDecision(JSON.parse(data.decision)); } catch {}
      } else if (data.decision) {
        setDecision(data.decision);
      }

      if (typeof data.critique === "string") {
        try { setCritique(JSON.parse(data.critique)); } catch {}
      } else if (data.critique) {
        setCritique(data.critique);
      }
    });

    return () => ws.close();
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>🏀 Live Shot Decision Dashboard</h2>
      {event && <EventCard event={event} />}
      <br />
      <DecisionCard decision={decision} critique={critique} />
    </div>
  );
}

export default App;