import { useState } from "react";

export default function App() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("home");
  const [confirmDelete, setConfirmDelete] = useState(false);

  const [createResponse, setCreateResponse] = useState(null);

  const [createForm, setCreateForm] = useState({
    name: "",
    email: "",
    phone_number: "",
    address: "",
    password: "",
    role: "customer",
  });

  const [updateForm, setUpdateForm] = useState({
  name: "",
  email: "",
  phone_number: "",
  address: "",
  password: "",
  role: "",
  });


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
      setUser(data)
      setTab("home");

    } catch (err) {
  setError(err.message || JSON.stringify(err));
}
  };

  const handleLogout = () => {
  setUser(null);
  setIdentifier("");
  setPassword("");
  setError("");
  setTab("home");
  };

  const loadMyAccount = async () => {
  setError("");

  try {
    const res = await fetch(`http://127.0.0.1:8000/users/${user.user_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to load account";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setUpdateForm({
      name: data.name,
      email: data.email,
      phone_number: data.phone_number,
      address: data.address,
      password: data.password,
      role: data.role,
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setError("");
    setCreateResponse(null);


      const { name, email, phone_number, address, password, role } = createForm;

      if (!name.trim()) return setError("Name is required");
      if (!email.trim()) return setError("Email is required");
      if (!phone_number.trim()) return setError("Phone number is required");
      if (!address.trim()) return setError("Address is required");
      if (!password.trim()) return setError("Password is required");
      if (!role) return setError("Role is required");


    try {
      const res = await fetch("http://127.0.0.1:8000/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(createForm),
      });

      const data = await res.json();

      if (!res.ok) {
        let msg = "User creation failed";

        if (typeof data.detail === "string") {
          msg = data.detail;
        } else if (Array.isArray(data.detail)) {
          msg = data.detail.map((x) => x.msg).join(", ");
        } else if (data.detail) {
          msg = JSON.stringify(data.detail);
        }

        throw new Error(msg);
      }

      setCreateResponse(data);
      setCreateForm({
        name: "",
        email: "",
        phone_number: "",
        address: "",
        password: "",
        role: "customer",
      });
    } catch (err) {
      setError(err.message || "Something went wrong");
    }
  };

 const handleUpdateUser = async (e) => {
  e.preventDefault();
  setError("");

  const { name, email, phone_number, address, password, role } = updateForm;

  if (!name.trim()) return setError("Name is required");
  if (!email.trim()) return setError("Email is required");
  if (!phone_number.trim()) return setError("Phone number is required");
  if (!address.trim()) return setError("Address is required");
  if (!password.trim()) return setError("Password is required");
  if (!role.trim()) return setError("Role is required");

  try {
    const payload = {
      ...updateForm,
      role: user.role, // 🔥 force original role
    };

    const res = await fetch(`http://127.0.0.1:8000/users/${user.user_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Update failed";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setUser({
      ...user,
      name: data.name,
      role: data.role,
    });

    setUpdateForm({
      ...updateForm,
      role: data.role,
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

  const handleDeleteUser = async () => {
  setError("");

  try {
    const res = await fetch(`http://127.0.0.1:8000/users/${user.user_id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    if (!res.ok) {
      let msg = "Delete failed";

      const data = await res.json().catch(() => null);

      if (typeof data?.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data?.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data?.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setUser(null);
    setConfirmDelete(false);
    setTab("home");
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

  if(!user) {
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

      <h2>Create User</h2>
      <form onSubmit={handleCreateUser}>
        <div>
          <input
            placeholder="Name"
            value={createForm.name}
            onChange={(e) =>
              setCreateForm({ ...createForm, name: e.target.value })
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            placeholder="Email"
            value={createForm.email}
            onChange={(e) =>
              setCreateForm({ ...createForm, email: e.target.value })
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            placeholder="Phone number"
            value={createForm.phone_number}
            onChange={(e) =>
              setCreateForm({ ...createForm, phone_number: e.target.value })
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            placeholder="Address"
            value={createForm.address}
            onChange={(e) =>
              setCreateForm({ ...createForm, address: e.target.value })
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            type="password"
            placeholder="Password"
            value={createForm.password}
            onChange={(e) =>
              setCreateForm({ ...createForm, password: e.target.value })
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <select
            value={createForm.role}
            onChange={(e) =>
              setCreateForm({ ...createForm, role: e.target.value })
            }
          >
            <option value="customer">customer</option>
            <option value="restaurant_owner">restaurant_owner</option>
            <option value="delivery_driver">delivery_driver</option>
          </select>
        </div>

        <button type="submit" style={{ marginTop: "1rem" }}>
          Create User
        </button>
      </form>

      {createResponse && (
        <div style={{ marginTop: "1rem", color: "green" }}>
          <p>User created successfully.</p>
          <p>Name: {createResponse.name}</p>
          <p>Email: {createResponse.email}</p>
          <p>Phone: {createResponse.phone_number}</p>
          <p>Address: {createResponse.address}</p>
          <p>Role: {createResponse.role}</p>
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

return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Main Page</h1>

      <p>Welcome {user.name}</p>
      <p>Role: {user.role}</p>
      <p>User ID: {user.user_id}</p>

      <div style={{ marginTop: "1rem", marginBottom: "1rem" }}>
        <button onClick={() => setTab("home")}>Home</button>

        <button
          onClick={() => {
            setTab("account");
            loadMyAccount();
          }}
          style={{ marginLeft: "0.5rem" }}
        >
          Account
        </button>

        <button onClick={handleLogout} style={{ marginLeft: "0.5rem" }}>
          Logout
        </button>
      </div>

      {tab === "home" && (
        <div>
          <h2>Home</h2>
          <p>This will be the main page.</p>
        </div>
      )}

      {tab === "account" && (
        <div>
          <h2>Update Account</h2>

          <form onSubmit={handleUpdateUser}>
            <div>
              <input
                placeholder="Name"
                value={updateForm.name}
                onChange={(e) =>
                  setUpdateForm({ ...updateForm, name: e.target.value })
                }
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}>
              <input
                placeholder="Email"
                value={updateForm.email}
                onChange={(e) =>
                  setUpdateForm({ ...updateForm, email: e.target.value })
                }
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}>
              <input
                placeholder="Phone number"
                value={updateForm.phone_number}
                onChange={(e) =>
                  setUpdateForm({
                    ...updateForm,
                    phone_number: e.target.value,
                  })
                }
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}>
              <input
                placeholder="Address"
                value={updateForm.address}
                onChange={(e) =>
                  setUpdateForm({ ...updateForm, address: e.target.value })
                }
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}>
              <input
                type="password"
                placeholder="Password"
                value={updateForm.password}
                onChange={(e) =>
                  setUpdateForm({ ...updateForm, password: e.target.value })
                }
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}></div>

            <button type="submit" style={{ marginTop: "1rem" }}>
              Update User
            </button>
          </form>
          <div style={{ marginTop: "1rem" }}>
          {!confirmDelete ? (
            <button
              type="button"
              onClick={() => setConfirmDelete(true)}
              style={{ backgroundColor: "red", color: "white" }}
            >
              Delete Account
            </button>
          ) : (
            <div>
              <p style={{ color: "red" }}>Are you sure?</p>

              <button
                type="button"
                onClick={handleDeleteUser}
                style={{ backgroundColor: "red", color: "white", marginRight: "0.5rem" }}
              >
                Yes, Delete
              </button>

              <button
                type="button"
                onClick={() => setConfirmDelete(false)}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
        </div>
      )}

      {error && (
        <p style={{ marginTop: "1rem", color: "red" }}>
          {error}
        </p>
      )}
    </div>
  );
}
