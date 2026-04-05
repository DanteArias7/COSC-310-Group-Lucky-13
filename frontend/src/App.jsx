import { useEffect, useRef, useState } from "react";

export default function App() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("home");
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const eventSourceRef = useRef(null);
  const [createResponse, setCreateResponse] = useState(null);
  const [restaurantTab, setRestaurantTab] = useState("create");
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

  const [restaurantResponse, setRestaurantResponse] = useState(null);

  const [restaurantForm, setRestaurantForm] = useState({
  name: "",
  phone_number: "",
  address: "",
  tags: "",
  hours: {
  Monday: { open: "", close: "", closed: false },
  Tuesday: { open: "", close: "", closed: false },
  Wednesday: { open: "", close: "", closed: false },
  Thursday: { open: "", close: "", closed: false },
  Friday: { open: "", close: "", closed: false },
  Saturday: { open: "", close: "", closed: false },
  Sunday: { open: "", close: "", closed: false },
},
  menu: [
    {
      name: "",
      price: "",
      description: "",
      tags: "",
    },
  ],
});

const [restaurantIdInput, setRestaurantIdInput] = useState("");
const [loadedRestaurant, setLoadedRestaurant] = useState(null);

const [updateRestaurantForm, setUpdateRestaurantForm] = useState({
  id: "",
  name: "",
  phone_number: "",
  address: "",
  tags: "",
  hours: {
    Monday: { open: "", close: "", closed: false },
    Tuesday: { open: "", close: "", closed: false },
    Wednesday: { open: "", close: "", closed: false },
    Thursday: { open: "", close: "", closed: false },
    Friday: { open: "", close: "", closed: false },
    Saturday: { open: "", close: "", closed: false },
    Sunday: { open: "", close: "", closed: false },
  },
});

const emptyHoursState = () => ({
  Monday: { open: "", close: "", closed: false },
  Tuesday: { open: "", close: "", closed: false },
  Wednesday: { open: "", close: "", closed: false },
  Thursday: { open: "", close: "", closed: false },
  Friday: { open: "", close: "", closed: false },
  Saturday: { open: "", close: "", closed: false },
  Sunday: { open: "", close: "", closed: false },
});

const convertApiHoursToFormHours = (hoursObj) => {
  const base = emptyHoursState();

  for (const day of Object.keys(base)) {
    const value = hoursObj?.[day];

    if (!value || value === "Closed") {
      base[day] = { open: "", close: "", closed: true };
    } else {
      const [open, close] = value.split("-");
      base[day] = {
        open: open || "",
        close: close || "",
        closed: false,
      };
    }
  }

  return base;
};

const convertFormHoursToApiHours = (hoursObj) =>
  Object.fromEntries(
    Object.entries(hoursObj).map(([day, val]) => [
      day,
      val.closed ? "Closed" : `${val.open}-${val.close}`,
    ])
  );

  const generateTimeOptions = () => {
  const times = [];
  for (let h = 0; h < 24; h++) {
    const hour = h.toString().padStart(2, "0");
    times.push(`${hour}:00`);
    times.push(`${hour}:30`);
  }
  return times;
};

  const timeOptions = generateTimeOptions();

  useEffect(() => {
      if (!user) return; // only start after login

      const es = new EventSource(
        `http://127.0.0.1:8000/notifications/stream?user_id=${user.user_id}`
      );

      eventSourceRef.current = es;

      es.addEventListener("notification", (event) => {
        setNotifications((prev) => [...prev, event.data]);
      });

      es.onerror = () => {
        console.error("SSE error");
      };

      return () => {
        es.close(); // cleanup on logout/unmount
      };
    }, [user]);

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

const handleRestaurantFieldChange = (field, value) => {
  setRestaurantForm((prev) => ({
    ...prev,
    [field]: value,
  }));
};

const handleMenuItemChange = (index, field, value) => {
  setRestaurantForm((prev) => {
    const updatedMenu = [...prev.menu];
    updatedMenu[index] = {
      ...updatedMenu[index],
      [field]: value,
    };
    return {
      ...prev,
      menu: updatedMenu,
    };
  });
};

const addMenuItem = () => {
  setRestaurantForm((prev) => ({
    ...prev,
    menu: [
      ...prev.menu,
      {
        name: "",
        price: "",
        description: "",
        tags: "",
      },
    ],
  }));
};

const removeMenuItem = (index) => {
  setRestaurantForm((prev) => ({
    ...prev,
    menu: prev.menu.filter((_, i) => i !== index),
  }));
};
const handleLoadRestaurantById = async (e) => {
  e.preventDefault();
  setError("");
  setLoadedRestaurant(null);

  if (!restaurantIdInput.trim()) {
    return setError("Restaurant ID is required");
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantIdInput}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to load restaurant";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setLoadedRestaurant(data);

    setUpdateRestaurantForm({
      id: data.id,
      name: data.name || "",
      phone_number: data.phone_number || "",
      address: data.address || "",
      tags: (data.tags || []).join(", "),
      hours: convertApiHoursToFormHours(data.hours || {}),
    });

    setRestaurantTab("update");
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const handleCreateRestaurant = async (e) => {
  e.preventDefault();
  setError("");
  setRestaurantResponse(null);

  if (!restaurantForm.name.trim()) return setError("Restaurant name is required");
  if (!/^\d{10}$/.test(restaurantForm.phone_number)) {
  return setError("Phone number must be exactly 10 digits");
}
    if (!/^\d+$/.test(restaurantForm.phone_number)) {
      return setError("Phone number must contain only digits");
} if (!restaurantForm.address.trim()) return setError("Address is required");
  if (restaurantForm.menu.length < 1) return setError("At least one menu item is required");

  for (const item of restaurantForm.menu) {
  if (!item.name.trim()) return setError("Each menu item must have a name");

  const price = Number(item.price);

  if (item.price === "" || isNaN(price)) {
    return setError("Each menu item must have a valid price");
  }

  if (price < 0) {
    return setError("Price cannot be negative");
  }

  if (!item.description.trim()) {
    return setError("Each menu item must have a description");
  }
}

  const payload = {
    name: restaurantForm.name,
    hours: Object.fromEntries(
  Object.entries(restaurantForm.hours).map(([day, val]) => [
    day,
    val.closed
      ? "Closed"
      : val.open && val.close
      ? `${val.open}-${val.close}`
      : "Closed",
  ])
),
    phone_number: restaurantForm.phone_number,
    address: restaurantForm.address,
    tags: restaurantForm.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
    menu: restaurantForm.menu.map((item) => ({
      name: item.name.trim(),
      price: Number(item.price),
      description: item.description.trim(),
      tags: item.tags
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
    })),
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/restaurants", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Restaurant creation failed";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setRestaurantResponse(data);

    setRestaurantForm({
      name: "",
      phone_number: "",
      address: "",
      tags: "",
      hours: {
        Monday: { open: "", close: "", closed: false },
        Tuesday: { open: "", close: "", closed: false },
        Wednesday: { open: "", close: "", closed: false },
        Thursday: { open: "", close: "", closed: false },
        Friday: { open: "", close: "", closed: false },
        Saturday: { open: "", close: "", closed: false },
        Sunday: { open: "", close: "", closed: false },
      },
      menu: [
        {
          name: "",
          price: "",
          description: "",
          tags: "",
        },
      ],
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const handleHoursChange = (day, field, value) => {
  setRestaurantForm((prev) => ({
    ...prev,
    hours: {
      ...prev.hours,
      [day]: {
        ...prev.hours[day],
        [field]: value,
      },
    },
  }));
};

const handleUpdateRestaurant = async (e) => {
  e.preventDefault();
  setError("");

  if (!updateRestaurantForm.id) {
    return setError("No restaurant loaded");
  }

  if (!updateRestaurantForm.name.trim()) {
    return setError("Restaurant name is required");
  }

  if (!/^\d+$/.test(updateRestaurantForm.phone_number)) {
    return setError("Phone number must contain only digits");
  }

  if (!updateRestaurantForm.address.trim()) {
    return setError("Address is required");
  }

  for (const [day, val] of Object.entries(updateRestaurantForm.hours)) {
    if (!val.closed && (!val.open || !val.close)) {
      return setError(`${day} must have both open and close times, or be marked closed`);
    }
  }

  const payload = {
    name: updateRestaurantForm.name,
    hours: convertFormHoursToApiHours(updateRestaurantForm.hours),
    phone_number: updateRestaurantForm.phone_number,
    address: updateRestaurantForm.address,
    tags: updateRestaurantForm.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
  };

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${updateRestaurantForm.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
        body: JSON.stringify(payload),
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Restaurant update failed";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setLoadedRestaurant(data);

    setUpdateRestaurantForm({
      id: data.id,
      name: data.name || "",
      phone_number: data.phone_number || "",
      address: data.address || "",
      tags: (data.tags || []).join(", "),
      hours: convertApiHoursToFormHours(data.hours || {}),
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const handleUpdateRestaurantFieldChange = (field, value) => {
  setUpdateRestaurantForm((prev) => ({
    ...prev,
    [field]: value,
  }));
};

const handleUpdateRestaurantHoursChange = (day, field, value) => {
  setUpdateRestaurantForm((prev) => ({
    ...prev,
    hours: {
      ...prev.hours,
      [day]: {
        ...prev.hours[day],
        [field]: value,
      },
    },
  }));
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

          {user.role === "restaurant_owner" && (
            <button
              onClick={() => {
                setTab("manage-restaurants");
                setRestaurantTab("create");
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              Manage Restaurants
            </button>
          )}

          <button
          onClick={() => setTab("notifications")}
          style={{ marginLeft: "0.5rem" }}
        >
          Notifications
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

     {tab === "manage-restaurants" && user.role === "restaurant_owner" && (
  <div>
    <h2>Manage Restaurants</h2>

    <div style={{ marginBottom: "1rem" }}>
      <button
        onClick={() => setRestaurantTab("create")}
      >
        Create Restaurant
      </button>
       <button
        onClick={() => setRestaurantTab("load")}
        style={{ marginLeft: "0.5rem" }}
      >
        Load Restaurant
      </button>

      <button
        onClick={() => setRestaurantTab("update")}
        style={{ marginLeft: "0.5rem" }}
      >
        Update Restaurant
      </button>
    </div>

    {restaurantTab === "create" && (
      <div>
        <h3>Create Restaurant</h3>

        <form onSubmit={handleCreateRestaurant}>
          <div>
            <input
              placeholder="Restaurant name"
              value={restaurantForm.name}
              onChange={(e) => handleRestaurantFieldChange("name", e.target.value)}
            />
          </div>

          <div style={{ marginTop: "0.5rem" }}>
           <input
            type="tel"
            inputMode="numeric"
            pattern="[0-9]*"
            maxLength={10}
            placeholder="Phone number"
            value={restaurantForm.phone_number}
            onChange={(e) => {
              const value = e.target.value.replace(/\D/g, "");
              handleRestaurantFieldChange("phone_number", value);
            }}
          />
          </div>

          <div style={{ marginTop: "0.5rem" }}>
            <input
              placeholder="Address"
              value={restaurantForm.address}
              onChange={(e) => handleRestaurantFieldChange("address", e.target.value)}
            />
          </div>

          <h3 style={{ marginTop: "1rem" }}>Hours</h3>

            <div style={{ marginLeft: "120px" }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "1rem",
                  fontWeight: "bold",
                  marginTop: "0.5rem",
                }}
              >
                <div style={{ width: "100px" }}></div>
                <div style={{ width: "140px" }}>Open</div>
                <div style={{ width: "140px" }}>Close</div>
                <div>Closed</div>
              </div>

              {Object.keys(restaurantForm.hours).map((day) => {
                const dayData = restaurantForm.hours[day];

                return (
                  <div
                    key={day}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "1rem",
                      marginTop: "0.5rem",
                    }}
                  >
                    <div style={{ width: "100px" }}>
                      <strong>{day}</strong>
                    </div>

                    <select
                      disabled={dayData.closed}
                      style={{ width: "140px" }}
                      value={dayData.open}
                      onChange={(e) => handleHoursChange(day, "open", e.target.value)}
                    >
                      <option value=""></option>
                      {timeOptions.map((t) => (
                        <option key={t} value={t}>{t}</option>
                      ))}
                    </select>

                    <select
                      disabled={dayData.closed}
                      style={{ width: "140px" }}
                      value={dayData.close}
                      onChange={(e) => handleHoursChange(day, "close", e.target.value)}
                    >
                      <option value=""></option>
                      {timeOptions.map((t) => (
                        <option key={t} value={t}>{t}</option>
                      ))}
                    </select>

                    <input
                      type="checkbox"
                      checked={dayData.closed}
                      onChange={(e) =>
                        handleHoursChange(day, "closed", e.target.checked)
                      }
                    />
                  </div>
                );
              })}
            </div>

            <div style={{ marginTop: "1rem" }}>
            <input
              placeholder="Restaurant tags (comma separated)"
              value={restaurantForm.tags}
              onChange={(e) => handleRestaurantFieldChange("tags", e.target.value)}
            />
          </div>

          <h3 style={{ marginTop: "1rem" }}>Menu</h3>

          {restaurantForm.menu.map((item, index) => (
            <div
              key={index}
              style={{
                border: "1px solid #ccc",
                padding: "1rem",
                marginTop: "1rem",
              }}
            >
              <p>Menu Item {index + 1}</p>

              <div>
                <input
                  placeholder="Item name"
                  value={item.name}
                  onChange={(e) =>
                    handleMenuItemChange(index, "name", e.target.value)
                  }
                />
              </div>

              <div style={{ marginTop: "0.5rem" }}>
                <input
                type="number"
                min="0"
                step="0.01"
                placeholder="Price"
                value={item.price}
                onKeyDown={(e) => {
                  if (e.key === "-" || e.key === "e") e.preventDefault();
                }}
                onChange={(e) => {
                  const value = e.target.value;
                  if (Number(value) < 0) return;
                  handleMenuItemChange(index, "price", value);
                }}
              />
              </div>

              <div style={{ marginTop: "0.5rem" }}>
                <input
                  placeholder="Description"
                  value={item.description}
                  onChange={(e) =>
                    handleMenuItemChange(index, "description", e.target.value)
                  }
                />
              </div>

              <div style={{ marginTop: "0.5rem" }}>
                <input
                  placeholder="Item tags (comma separated)"
                  value={item.tags}
                  onChange={(e) =>
                    handleMenuItemChange(index, "tags", e.target.value)
                  }
                />
              </div>

              {restaurantForm.menu.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeMenuItem(index)}
                  style={{ marginTop: "0.5rem" }}
                >
                  Remove Item
                </button>
              )}
            </div>
          ))}

          <button
            type="button"
            onClick={addMenuItem}
            style={{ marginTop: "1rem", marginRight: "0.5rem" }}
          >
            Add Menu Item
          </button>

          <button type="submit" style={{ marginTop: "1rem" }}>
            Create Restaurant
          </button>
        </form>

        {restaurantResponse && (
          <div style={{ marginTop: "1rem", color: "green" }}>
            <p>Restaurant created successfully.</p>
            <p>ID: {restaurantResponse.id}</p>
            <p>Name: {restaurantResponse.name}</p>
            <p>Owner User ID: {restaurantResponse.user_id}</p>
          </div>
        )}
      </div>
    )}

    {restaurantTab === "load" && (
  <div>
    <h3>Load Restaurant</h3>

    <form onSubmit={handleLoadRestaurantById}>
      <input
        type="number"
        min="1"
        placeholder="Restaurant ID"
        value={restaurantIdInput}
        onChange={(e) => setRestaurantIdInput(e.target.value)}
      />

      <button type="submit" style={{ marginLeft: "0.5rem" }}>
        Load
      </button>
    </form>

    {loadedRestaurant && (
      <div style={{ marginTop: "1rem" }}>
        <p><strong>ID:</strong> {loadedRestaurant.id}</p>
        <p><strong>Name:</strong> {loadedRestaurant.name}</p>
        <p><strong>Owner User ID:</strong> {loadedRestaurant.user_id}</p>
        <p><strong>Phone:</strong> {loadedRestaurant.phone_number}</p>
        <p><strong>Address:</strong> {loadedRestaurant.address}</p>
        <p><strong>Tags:</strong> {(loadedRestaurant.tags || []).join(", ")}</p>
        <p><strong>Average Rating:</strong> {String(loadedRestaurant.average_rating)}</p>
      </div>
    )}
  </div>
)}

{restaurantTab === "update" && (
  <div>
    <h3>Update Restaurant</h3>

    {!updateRestaurantForm.id ? (
      <p>Load a restaurant first.</p>
    ) : (
      <form onSubmit={handleUpdateRestaurant}>
        <div>
          <input
            placeholder="Restaurant name"
            value={updateRestaurantForm.name}
            onChange={(e) =>
              handleUpdateRestaurantFieldChange("name", e.target.value)
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            type="tel"
            inputMode="numeric"
            pattern="[0-9]*"
            placeholder="Phone number"
            value={updateRestaurantForm.phone_number}
            onChange={(e) =>
              handleUpdateRestaurantFieldChange(
                "phone_number",
                e.target.value.replace(/\D/g, "")
              )
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            placeholder="Address"
            value={updateRestaurantForm.address}
            onChange={(e) =>
              handleUpdateRestaurantFieldChange("address", e.target.value)
            }
          />
        </div>

        <div style={{ marginTop: "0.5rem" }}>
          <input
            placeholder="Restaurant tags (comma separated)"
            value={updateRestaurantForm.tags}
            onChange={(e) =>
              handleUpdateRestaurantFieldChange("tags", e.target.value)
            }
          />
        </div>

        <h3 style={{ marginTop: "1rem" }}>Hours</h3>

        <div style={{ marginLeft: "120px" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "1rem",
              fontWeight: "bold",
              marginTop: "0.5rem",
            }}
          >
            <div style={{ width: "100px" }}></div>
            <div style={{ width: "140px" }}>Open</div>
            <div style={{ width: "140px" }}>Close</div>
            <div>Closed</div>
          </div>

          {Object.keys(updateRestaurantForm.hours).map((day) => {
            const dayData = updateRestaurantForm.hours[day];

            return (
              <div
                key={day}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "1rem",
                  marginTop: "0.5rem",
                }}
              >
                <div style={{ width: "100px" }}>
                  <strong>{day}</strong>
                </div>

                <select
                  disabled={dayData.closed}
                  style={{ width: "140px" }}
                  value={dayData.open}
                  onChange={(e) =>
                    handleUpdateRestaurantHoursChange(day, "open", e.target.value)
                  }
                >
                  <option value=""></option>
                  {timeOptions.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>

                <select
                  disabled={dayData.closed}
                  style={{ width: "140px" }}
                  value={dayData.close}
                  onChange={(e) =>
                    handleUpdateRestaurantHoursChange(day, "close", e.target.value)
                  }
                >
                  <option value=""></option>
                  {timeOptions.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>

                <input
                  type="checkbox"
                  checked={dayData.closed}
                  onChange={(e) =>
                    handleUpdateRestaurantHoursChange(day, "closed", e.target.checked)
                  }
                />
              </div>
            );
          })}
        </div>

        <button type="submit" style={{ marginTop: "1rem" }}>
          Update Restaurant
        </button>
      </form>
    )}
  </div>
)}
  </div>
)}
            {tab === "notifications" && (
        <div>
          <h2>Notifications</h2>

          {notifications.length === 0 ? (
            <p>No notifications yet.</p>
          ) : (
            <ul>
              {notifications.map((notification, index) => (
                <li key={index}>{notification}</li>
              ))}
            </ul>
          )}
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
