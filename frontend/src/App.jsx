import { useState } from "react";

export default function App() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setResponse("");

    const payload = {
    identifier,
    password,
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/login/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        let msg = "Login failed";

          if (typeof data.detail === "string") {
            msg = data.detail;
          } else if (Array.isArray(data.detail)) {
            msg = data.detail.map(x => x.msg).join(", ");
          } else if (data.detail) {
            msg = JSON.stringify(data.detail);
          }

          throw new Error(msg);
      }

      setResponse(data);

    } catch (err) {
  setError(err.message || JSON.stringify(err));
}
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Login</h1>

      <form onSubmit={handleLogin}>
        <div>
          <input
            placeholder="Email or phone"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit" style={{ marginTop: "1rem" }}>
          Login
        </button>
      </form>

      {response && (
        <div style={{ marginTop: "1rem", color: "green" }}>
          <p>Welcome {response.name}</p>
          <p>Role: {response.role}</p>
          <p>User ID: {response.user_id}</p>
        </div>
      )}

      {error && (
      <p style={{ color: "red" }}>
        {typeof error === "string" ? error : JSON.stringify(error)}
      </p>
    )}
    </div>
  );
}