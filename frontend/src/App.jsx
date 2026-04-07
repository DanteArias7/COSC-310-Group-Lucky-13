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
  const [confirmDeleteRestaurant, setConfirmDeleteRestaurant] = useState(false);
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

const [menuItemResponse, setMenuItemResponse] = useState(null);

const [addMenuItemForm, setAddMenuItemForm] = useState({
  restaurant_id: "",
  name: "",
  price: "",
  description: "",
  tags: "",
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

const [updateMenuItemResponse, setUpdateMenuItemResponse] = useState(null);

const [updateMenuItemForm, setUpdateMenuItemForm] = useState({
  restaurant_id: "",
  menu_item_id: "",
  name: "",
  price: "",
  description: "",
  tags: "",
  item_status: "",
});

const [confirmDeleteMenuItem, setConfirmDeleteMenuItem] = useState(false);

const [deleteMenuItemForm, setDeleteMenuItemForm] = useState({
  restaurant_id: "",
  menu_item_id: "",
});

const [deleteMenuItemResponse, setDeleteMenuItemResponse] = useState(null);

const [favorites, setFavorites] = useState([]);
const [favoriteTab, setFavoriteTab] = useState("view");
const [favoriteForm, setFavoriteForm] = useState({
  restaurant_id: "",
  menu_item_id: "",
});

const [browseData, setBrowseData] = useState({
  items: [],
  total: 0,
  page: 1,
  size: 50,
  pages: 1,
});

const [browseSearch, setBrowseSearch] = useState("");
const [browseTagsInput, setBrowseTagsInput] = useState("");
const [browseLoading, setBrowseLoading] = useState(false);

const [selectedBrowseRestaurant, setSelectedBrowseRestaurant] = useState(null);
const [browseDetailLoading, setBrowseDetailLoading] = useState(false);

const [cartResponse, setCartResponse] = useState(null);
const [cartLoading, setCartLoading] = useState(false);

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

const [addToCartLoading, setAddToCartLoading] = useState(false);
const [cartMessage, setCartMessage] = useState("");
const [removeFromCartLoading, setRemoveFromCartLoading] = useState(false);

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

  const [browseMenuData, setBrowseMenuData] = useState({
  items: [],
  total: 0,
  page: 1,
  size: 50,
  pages: 1,
});

const [browseMenuSearch, setBrowseMenuSearch] = useState("");
const [browseMenuTagsInput, setBrowseMenuTagsInput] = useState("");
const [browseMenuPriceMin, setBrowseMenuPriceMin] = useState("");
const [browseMenuPriceMax, setBrowseMenuPriceMax] = useState("");
const [browseMenuLoading, setBrowseMenuLoading] = useState(false);

const [ratingForm, setRatingForm] = useState({
  rating: "5.0",
  review: "",
});

const [ratingLoading, setRatingLoading] = useState(false);
const [ratingResponse, setRatingResponse] = useState(null);

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
      setFavorites([]);
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

const handleDeleteRestaurant = async () => {
  setError("");

  const idToDelete = loadedRestaurant?.id || restaurantIdInput;

  if (!idToDelete) {
    return setError("Load a restaurant or enter a restaurant ID first");
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/restaurants/${idToDelete}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    if (!res.ok) {
      let msg = "Restaurant delete failed";

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

    setLoadedRestaurant(null);
    setRestaurantIdInput("");
    setConfirmDeleteRestaurant(false);

    setUpdateRestaurantForm({
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

    setRestaurantResponse({ deleted: true, id: idToDelete });
    setRestaurantTab("delete");
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const handleAddMenuItemFieldChange = (field, value) => {
  setAddMenuItemForm((prev) => ({
    ...prev,
    [field]: value,
  }));
};

const handleAddMenuItemToRestaurant = async (e) => {
  e.preventDefault();
  setError("");
  setMenuItemResponse(null);

  const restaurantId = addMenuItemForm.restaurant_id || loadedRestaurant?.id;

  if (!restaurantId) {
    return setError("Restaurant ID is required");
  }

  if (!addMenuItemForm.name.trim()) {
    return setError("Menu item name is required");
  }

  const price = Number(addMenuItemForm.price);

  if (addMenuItemForm.price === "" || isNaN(price)) {
    return setError("Menu item price must be valid");
  }

  if (price < 0) {
    return setError("Price cannot be negative");
  }

  if (!addMenuItemForm.description.trim()) {
    return setError("Menu item description is required");
  }

  const payload = {
    name: addMenuItemForm.name.trim(),
    price,
    description: addMenuItemForm.description.trim(),
    tags: addMenuItemForm.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
  };

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${restaurantId}/menu`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
        body: JSON.stringify(payload),
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to add menu item";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setMenuItemResponse(data);

    setAddMenuItemForm({
      restaurant_id: restaurantId.toString(),
      name: "",
      price: "",
      description: "",
      tags: "",
    });

    if (loadedRestaurant) {
      setLoadedRestaurant({
        ...loadedRestaurant,
        menu: [...(loadedRestaurant.menu || []), data],
      });
    }
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

  const handleUpdateMenuItemFieldChange = (field, value) => {
  setUpdateMenuItemForm((prev) => ({
    ...prev,
    [field]: value,
  }));
};

const handleUpdateMenuItem = async (e) => {
  e.preventDefault();
  setError("");
  setUpdateMenuItemResponse(null);

  if (!updateMenuItemForm.restaurant_id.trim()) {
    return setError("Restaurant ID is required");
  }

  if (!updateMenuItemForm.menu_item_id.trim()) {
    return setError("Menu item ID is required");
  }

  if (!updateMenuItemForm.name.trim()) {
    return setError("Menu item name is required");
  }

  const price = Number(updateMenuItemForm.price);

  if (updateMenuItemForm.price === "" || isNaN(price)) {
    return setError("Menu item price must be valid");
  }

  if (price < 0) {
    return setError("Price cannot be negative");
  }

  if (!updateMenuItemForm.description.trim()) {
    return setError("Menu item description is required");
  }

  const payload = {
    name: updateMenuItemForm.name.trim(),
    price,
    description: updateMenuItemForm.description.trim(),
    tags: updateMenuItemForm.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
  };

  const query = updateMenuItemForm.item_status.trim()
    ? `?item_status=${encodeURIComponent(updateMenuItemForm.item_status.trim())}`
    : "";

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${updateMenuItemForm.restaurant_id}/menu/${updateMenuItemForm.menu_item_id}${query}`,
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
      let msg = "Failed to update menu item";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setUpdateMenuItemResponse(data);

    if (loadedRestaurant && String(loadedRestaurant.id) === String(updateMenuItemForm.restaurant_id)) {
      setLoadedRestaurant({
        ...loadedRestaurant,
        menu: (loadedRestaurant.menu || []).map((item) =>
          String(item.id) === String(updateMenuItemForm.menu_item_id) ? data : item
        ),
      });
    }
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const loadMenuItemIntoUpdateForm = (menuItem) => {
  setUpdateMenuItemForm({
    restaurant_id: loadedRestaurant ? String(loadedRestaurant.id) : "",
    menu_item_id: menuItem.id,
    name: menuItem.name || "",
    price: String(menuItem.price ?? ""),
    description: menuItem.description || "",
    tags: (menuItem.tags || []).join(", "),
    item_status: menuItem.status || "",
  });
  setRestaurantTab("update-menu-item");
};

const handleDeleteMenuItemFieldChange = (field, value) => {
  setDeleteMenuItemForm((prev) => ({
    ...prev,
    [field]: value,
  }));
};

const handleDeleteMenuItem = async () => {
  setError("");
  setDeleteMenuItemResponse(null);

  const restaurantId = deleteMenuItemForm.restaurant_id || loadedRestaurant?.id;

  if (!restaurantId) {
    return setError("Restaurant ID is required");
  }

  if (!deleteMenuItemForm.menu_item_id.trim()) {
    return setError("Menu item ID is required");
  }

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${restaurantId}/menu/${deleteMenuItemForm.menu_item_id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    if (!res.ok) {
      let msg = "Failed to delete menu item";

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

    setDeleteMenuItemResponse({
      deleted: true,
      restaurant_id: String(restaurantId),
      menu_item_id: deleteMenuItemForm.menu_item_id,
    });

    if (loadedRestaurant && String(loadedRestaurant.id) === String(restaurantId)) {
      setLoadedRestaurant({
        ...loadedRestaurant,
        menu: (loadedRestaurant.menu || []).filter(
          (item) => String(item.id) !== String(deleteMenuItemForm.menu_item_id)
        ),
      });
    }

    setDeleteMenuItemForm({
      restaurant_id: String(restaurantId),
      menu_item_id: "",
    });

    setConfirmDeleteMenuItem(false);
  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const loadMenuItemIntoDeleteForm = (menuItem) => {
  setDeleteMenuItemForm({
    restaurant_id: loadedRestaurant ? String(loadedRestaurant.id) : "",
    menu_item_id: menuItem.id,
  });
  setDeleteMenuItemResponse(null);
  setConfirmDeleteMenuItem(false);
  setRestaurantTab("delete-menu-item");
};

const getMenuItemName = async (restaurantId, menuItemId) => {
  const res = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}`, {
    headers: {
      "Content-Type": "application/json",
      "user-id": user.user_id,
    },
  });

  const data = await res.json();

  const item = data.menu.find((i) => i.id === menuItemId);
  return item ? item.name : "Unknown item";
};

const loadFavorites = async () => {
  setFavorites([]);
  try {
    const res = await fetch("http://127.0.0.1:8000/favorites", {
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

if (!Array.isArray(data)) {
  setFavorites([]);
  return;
}



    const enriched = await Promise.all(
      data.map(async (fav) => {
        const res = await fetch(
          `http://127.0.0.1:8000/restaurants/${fav.restaurant_id}`,
          {
            headers: {
              "Content-Type": "application/json",
              "user-id": user.user_id,
            },
          }
        );

        const restaurant = await res.json();

        const item = restaurant.menu.find(
          (i) => i.id === fav.menu_item_id
        );

        return {
          ...fav,
          menu_item_name: item?.name || "Unknown",
          restaurant_name: restaurant.name || "Unknown",
        };
      })
    );

    setFavorites(enriched);
  } catch (err) {
    setError(err.message);
  }
};

const handleAddFavorite = async (e) => {
  e.preventDefault();
  setError("");

  try {
    const payload = {
      id: crypto.randomUUID(),
      user_id: user.user_id,
      restaurant_id: Number(favoriteForm.restaurant_id),
      menu_item_id: favoriteForm.menu_item_id,
    };

    const res = await fetch("http://127.0.0.1:8000/favorites", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to add favorite";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    // ✅ success
    setFavoriteForm({
      restaurant_id: "",
      menu_item_id: "",
    });

    // optional refresh
    setFavoriteTab("view");
    loadFavorites();

  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const handleDeleteFavorite = async (favoriteId) => {
  setError("");

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/favorites/${favoriteId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    if (!res.ok) {
      const data = await res.json().catch(() => null);

      let msg = "Delete failed";

      if (typeof data?.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data?.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data?.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    loadFavorites();

  } catch (err) {
    setError(err.message || "Something went wrong");
  }
};

const loadBrowseRestaurants = async (page = 1) => {
  if (!user || user.role !== "customer") return;

  setError("");
  setBrowseLoading(true);

  try {
    const params = new URLSearchParams();
    params.append("page", String(page));

    if (browseSearch.trim()) {
      params.append("search", browseSearch.trim());
    }

    const tagList = browseTagsInput
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);

    tagList.forEach((tag) => params.append("tags", tag));

    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/browse?${params.toString()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to browse restaurants";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setBrowseData({
      items: data.items || [],
      total: data.total || 0,
      page: data.page || 1,
      size: data.size || 50,
      pages: data.pages || 1,
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setBrowseLoading(false);
  }
};


const loadBrowseRestaurantDetails = async (restaurantId) => {
  if (!user) return;

  setError("");
  setCartResponse(null);
  setCartMessage("");
  setBrowseDetailLoading(true);

  setBrowseMenuData({
    items: [],
    total: 0,
    page: 1,
    size: 50,
    pages: 1,
  });
  setBrowseMenuSearch("");
  setBrowseMenuTagsInput("");
  setBrowseMenuPriceMin("");
  setBrowseMenuPriceMax("");

  setRatingResponse(null);
setRatingForm({
  rating: "5.0",
  review: "",
});

  try {
    const res = await fetch(`http://127.0.0.1:8000/restaurants/${restaurantId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to load restaurant details";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setSelectedBrowseRestaurant(data);
    await loadBrowseRestaurantMenu(restaurantId, 1);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setBrowseDetailLoading(false);
  }
};

const handleStartCart = async (restaurantId) => {
  if (!user || user.role !== "customer") return;

  setError("");
  setCartMessage("");
  setCartResponse(null);
  setCartLoading(true);

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${restaurantId}/cart`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to start cart";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setCartResponse(data);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setCartLoading(false);
  }
};


const handleAddItemToCart = async (menuItem) => {
  if (!user || user.role !== "customer") return;

  if (!cartResponse?.id) {
    return setError("Start a cart first for this restaurant");
  }

  setError("");
  setCartMessage("");
  setAddToCartLoading(true);

  try {
    const payload = {
  ...menuItem,
};

    const res = await fetch(
  `http://127.0.0.1:8000/restaurants/${selectedBrowseRestaurant.id}/cart/${cartResponse.id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
        body: JSON.stringify(payload),
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to add item to cart";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setCartResponse(data);
    setCartMessage(`${menuItem.name} added to cart.`);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setAddToCartLoading(false);
  }
};

const handleRemoveItemFromCart = async (menuItemId) => {
  if (!user || user.role !== "customer") return;

  if (!cartResponse?.id) {
    return setError("No active cart found");
  }

  if (!selectedBrowseRestaurant?.id) {
    return setError("Load a restaurant first");
  }

  setError("");
  setCartMessage("");
  setRemoveFromCartLoading(true);

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${selectedBrowseRestaurant.id}/cart/${cartResponse.id}/${menuItemId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    if (!res.ok) {
      let msg = "Failed to remove item from cart";

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

    setCartResponse((prev) => {
      if (!prev) return prev;

      const updatedItems = (prev.cart_items || [])
        .map((cartItem) => {
          if (String(cartItem.item?.id) !== String(menuItemId)) {
            return cartItem;
          }

          const currentQty = Number(cartItem.quantity || 0);
          const nextQty = currentQty - 1;

          if (nextQty <= 0) {
            return null;
          }

          return {
            ...cartItem,
            quantity: nextQty,
          };
        })
        .filter(Boolean);

      const subtotal = updatedItems.reduce((sum, cartItem) => {
        const price = Number(cartItem.item?.price || 0);
        const qty = Number(cartItem.quantity || 0);
        return sum + price * qty;
      }, 0);


      const deliveryFee = Number(prev.delivery_fee || 0);
      const taxRate = subtotal > 0 && Number(prev.subtotal || 0) > 0
        ? Number(prev.tax || 0) / Number(prev.subtotal || 1)
        : 0;
      const tax = subtotal * taxRate;
      const total = subtotal + deliveryFee + tax;

      return {
        ...prev,
        cart_items: updatedItems,
        subtotal: Number(subtotal.toFixed(2)),
        tax: Number(tax.toFixed(2)),
        total: Number(total.toFixed(2)),
      };
    });

    setCartMessage("Item quantity updated.");
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setRemoveFromCartLoading(false);
  }
};

const loadBrowseRestaurantMenu = async (restaurantId, page = 1) => {
  if (!user) return;

  setError("");
  setBrowseMenuLoading(true);

  try {
    const params = new URLSearchParams();
    params.append("page", String(page));

    if (browseMenuSearch.trim()) {
      params.append("search", browseMenuSearch.trim());
    }

    if (browseMenuPriceMin !== "") {
      params.append("price_min", String(browseMenuPriceMin));
    }

    if (browseMenuPriceMax !== "") {
      params.append("price_max", String(browseMenuPriceMax));
    }

    const tagList = browseMenuTagsInput
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);

    tagList.forEach((tag) => params.append("tags", tag));

    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${restaurantId}/menu?${params.toString()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to load restaurant menu";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setBrowseMenuData({
      items: data.items || [],
      total: data.total || 0,
      page: data.page || 1,
      size: data.size || 50,
      pages: data.pages || 1,
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setBrowseMenuLoading(false);
  }
};

// === ADD THIS near your other handler functions ===
const handleAddRating = async (e) => {
  e.preventDefault();

  if (!user || user.role !== "customer") return;

  if (!selectedBrowseRestaurant?.id) {
    return setError("Load a restaurant first");
  }

  if (!ratingForm.review.trim()) {
    return setError("Review is required");
  }

  const numericRating = Number(ratingForm.rating);

  if (isNaN(numericRating) || numericRating < 0.5 || numericRating > 5.0) {
    return setError("Rating must be between 0.5 and 5.0");
  }

  setError("");
  setRatingResponse(null);
  setRatingLoading(true);

  try {
    const payload = {
      customer_id: user.user_id,
      rating: numericRating,
      review: ratingForm.review.trim(),
    };

    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${selectedBrowseRestaurant.id}/rate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
        body: JSON.stringify(payload),
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to add rating";

      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }

      throw new Error(msg);
    }

    setRatingResponse(data);

    setRatingForm({
      rating: "5.0",
      review: "",
    });

    // Update selected restaurant locally so the new rating appears immediately
    setSelectedBrowseRestaurant((prev) => {
      if (!prev) return prev;

      const existingRatings = prev.ratings || [];
      const updatedRatings = [...existingRatings, data];

      const validRatings = updatedRatings
        .map((r) => Number(r.rating))
        .filter((n) => !isNaN(n));

      const average =
        validRatings.length > 0
          ? validRatings.reduce((sum, n) => sum + n, 0) / validRatings.length
          : null;

      return {
        ...prev,
        ratings: updatedRatings,
        average_rating: average !== null ? Number(average.toFixed(2)) : null,
      };
    });
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setRatingLoading(false);
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

            {user.role === "customer" && (
            <button
            onClick={() => {
              setTab("browse");
              setSelectedBrowseRestaurant(null);
              setCartResponse(null);
              loadBrowseRestaurants(1);
            }}
            style={{ marginLeft: "0.5rem" }}
          >
            Browse Restaurants
          </button>
          )}

            {user.role === "customer" && (
          <button
          onClick={() => {
          setTab("favorites");
          setFavoriteTab(null);
          setFavorites([]);
          }}
          style={{ marginLeft: "0.5rem" }}
          >
          Favorites
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
      <button
        onClick={() => {
          setRestaurantTab("add-menu-item");
          setAddMenuItemForm((prev) => ({
            ...prev,
            restaurant_id: loadedRestaurant?.id ? String(loadedRestaurant.id) : prev.restaurant_id,
          }));
        }}
        style={{ marginLeft: "0.5rem" }}
      >
        Add Menu Item
      </button>
        <button
        onClick={() => {
          setRestaurantTab("update-menu-item");
          setUpdateMenuItemForm((prev) => ({
            ...prev,
            restaurant_id: loadedRestaurant?.id ? String(loadedRestaurant.id) : prev.restaurant_id,
          }));
        }}
        style={{ marginLeft: "0.5rem" }}
      >
        Update Menu Item
      </button>
      <button
        onClick={() => {
          setRestaurantTab("delete-menu-item");
          setConfirmDeleteMenuItem(false);
          setDeleteMenuItemResponse(null);
          setDeleteMenuItemForm((prev) => ({
            ...prev,
            restaurant_id: loadedRestaurant?.id ? String(loadedRestaurant.id) : prev.restaurant_id,
          }));
        }}
        style={{ marginLeft: "0.5rem" }}
      >
        Delete Menu Item
      </button>
      <button
        onClick={() => {
          setRestaurantTab("delete");
          setConfirmDeleteRestaurant(false);
        }}
        style={{ marginLeft: "0.5rem" }}
      >
        Delete Restaurant
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
    {loadedRestaurant?.menu?.length > 0 && (
  <div style={{ marginTop: "1rem" }}>
    <h4>Menu</h4>
    {loadedRestaurant.menu.map((item) => (
      <div
        key={item.id}
        style={{
          border: "1px solid #ccc",
          padding: "0.75rem",
          marginTop: "0.5rem",
        }}
      >
        <p><strong>ID:</strong> {item.id}</p>
        <p><strong>Name:</strong> {item.name}</p>
        <p><strong>Price:</strong> {item.price}</p>
        <p><strong>Status:</strong> {item.status}</p>

        <button
          type="button"
          onClick={() => loadMenuItemIntoUpdateForm(item)}
        >
          Edit This Menu Item
        </button>

        <button
      type="button"
      onClick={() => loadMenuItemIntoDeleteForm(item)}
      style={{ marginLeft: "0.5rem" }}
    >
      Delete This Menu Item
    </button>
      </div>
    ))}
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

{restaurantTab === "add-menu-item" && (
  <div>
    <h3>Add Menu Item</h3>

    <form onSubmit={handleAddMenuItemToRestaurant}>
      <div>
        <input
          type="number"
          min="1"
          placeholder="Restaurant ID"
          value={addMenuItemForm.restaurant_id}
          onChange={(e) =>
            handleAddMenuItemFieldChange("restaurant_id", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Menu item name"
          value={addMenuItemForm.name}
          onChange={(e) =>
            handleAddMenuItemFieldChange("name", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          type="number"
          min="0"
          step="0.01"
          placeholder="Price"
          value={addMenuItemForm.price}
          onKeyDown={(e) => {
            if (e.key === "-" || e.key === "e") e.preventDefault();
          }}
          onChange={(e) => {
            const value = e.target.value;
            if (Number(value) < 0) return;
            handleAddMenuItemFieldChange("price", value);
          }}
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Description"
          value={addMenuItemForm.description}
          onChange={(e) =>
            handleAddMenuItemFieldChange("description", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Tags (comma separated)"
          value={addMenuItemForm.tags}
          onChange={(e) =>
            handleAddMenuItemFieldChange("tags", e.target.value)
          }
        />
      </div>

      <button type="submit" style={{ marginTop: "1rem" }}>
        Add Menu Item
      </button>
    </form>

    {menuItemResponse && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Menu item added successfully.</p>
        <p>ID: {menuItemResponse.id}</p>
        <p>Name: {menuItemResponse.name}</p>
        <p>Price: {menuItemResponse.price}</p>
        <p>Description: {menuItemResponse.description}</p>
        <p>Status: {menuItemResponse.status}</p>
        <p>Tags: {(menuItemResponse.tags || []).join(", ")}</p>
      </div>
    )}
  </div>
)}

{restaurantTab === "update-menu-item" && (
  <div>
    <h3>Update Menu Item</h3>

    <form onSubmit={handleUpdateMenuItem}>
      <div>
        <input
          type="number"
          min="1"
          placeholder="Restaurant ID"
          value={updateMenuItemForm.restaurant_id}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("restaurant_id", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Menu Item ID"
          value={updateMenuItemForm.menu_item_id}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("menu_item_id", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Menu item name"
          value={updateMenuItemForm.name}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("name", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          type="number"
          min="0"
          step="0.01"
          placeholder="Price"
          value={updateMenuItemForm.price}
          onKeyDown={(e) => {
            if (e.key === "-" || e.key === "e") e.preventDefault();
          }}
          onChange={(e) => {
            const value = e.target.value;
            if (Number(value) < 0) return;
            handleUpdateMenuItemFieldChange("price", value);
          }}
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Description"
          value={updateMenuItemForm.description}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("description", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Tags (comma separated)"
          value={updateMenuItemForm.tags}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("tags", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder='Optional status, e.g. "Available" or "Unavailable"'
          value={updateMenuItemForm.item_status}
          onChange={(e) =>
            handleUpdateMenuItemFieldChange("item_status", e.target.value)
          }
        />
      </div>

      <button type="submit" style={{ marginTop: "1rem" }}>
        Update Menu Item
      </button>
    </form>

    {updateMenuItemResponse && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Menu item updated successfully.</p>
        <p>ID: {updateMenuItemResponse.id}</p>
        <p>Name: {updateMenuItemResponse.name}</p>
        <p>Price: {updateMenuItemResponse.price}</p>
        <p>Description: {updateMenuItemResponse.description}</p>
        <p>Status: {updateMenuItemResponse.status}</p>
        <p>Tags: {(updateMenuItemResponse.tags || []).join(", ")}</p>
      </div>
    )}
  </div>
)}

{restaurantTab === "delete-menu-item" && (
  <div>
    <h3>Delete Menu Item</h3>

    <form
      onSubmit={(e) => {
        e.preventDefault();
        setConfirmDeleteMenuItem(true);
      }}
    >
      <div>
        <input
          type="number"
          min="1"
          placeholder="Restaurant ID"
          value={deleteMenuItemForm.restaurant_id}
          onChange={(e) =>
            handleDeleteMenuItemFieldChange("restaurant_id", e.target.value)
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Menu Item ID"
          value={deleteMenuItemForm.menu_item_id}
          onChange={(e) =>
            handleDeleteMenuItemFieldChange("menu_item_id", e.target.value)
          }
        />
      </div>

      <button type="submit" style={{ marginTop: "1rem" }}>
        Select Menu Item
      </button>
    </form>

    {(deleteMenuItemForm.restaurant_id || loadedRestaurant?.id) &&
      deleteMenuItemForm.menu_item_id && (
        <div style={{ marginTop: "1rem" }}>
          {!confirmDeleteMenuItem ? (
            <button
              type="button"
              onClick={() => setConfirmDeleteMenuItem(true)}
              style={{ backgroundColor: "red", color: "white" }}
            >
              Delete Menu Item
            </button>
          ) : (
            <div>
              <p style={{ color: "red" }}>
                Are you sure you want to delete this menu item?
              </p>

              <button
                type="button"
                onClick={handleDeleteMenuItem}
                style={{
                  backgroundColor: "red",
                  color: "white",
                  marginRight: "0.5rem",
                }}
              >
                Yes, Delete
              </button>

              <button
                type="button"
                onClick={() => setConfirmDeleteMenuItem(false)}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}

    {deleteMenuItemResponse?.deleted && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Menu item deleted successfully.</p>
        <p>Restaurant ID: {deleteMenuItemResponse.restaurant_id}</p>
        <p>Menu Item ID: {deleteMenuItemResponse.menu_item_id}</p>
      </div>
    )}
  </div>
)}

{restaurantTab === "delete" && (
  <div>
    <h3>Delete Restaurant</h3>

    <form
      onSubmit={(e) => {
        e.preventDefault();
        setConfirmDeleteRestaurant(true);
      }}
    >
      <input
        type="number"
        min="1"
        placeholder="Restaurant ID"
        value={restaurantIdInput}
        onChange={(e) => setRestaurantIdInput(e.target.value)}
      />

      <button type="submit" style={{ marginLeft: "0.5rem" }}>
        Select Restaurant
      </button>
    </form>

    {loadedRestaurant && (
      <div style={{ marginTop: "1rem" }}>
        <p><strong>ID:</strong> {loadedRestaurant.id}</p>
        <p><strong>Name:</strong> {loadedRestaurant.name}</p>
        <p><strong>Owner User ID:</strong> {loadedRestaurant.user_id}</p>
        <p><strong>Phone:</strong> {loadedRestaurant.phone_number}</p>
        <p><strong>Address:</strong> {loadedRestaurant.address}</p>
      </div>
    )}

    {(restaurantIdInput || loadedRestaurant?.id) && (
      <div style={{ marginTop: "1rem" }}>
        {!confirmDeleteRestaurant ? (
          <button
            type="button"
            onClick={() => setConfirmDeleteRestaurant(true)}
            style={{ backgroundColor: "red", color: "white" }}
          >
            Delete Restaurant
          </button>
        ) : (
          <div>
            <p style={{ color: "red" }}>
              Are you sure you want to delete this restaurant?
            </p>

            <button
              type="button"
              onClick={handleDeleteRestaurant}
              style={{
                backgroundColor: "red",
                color: "white",
                marginRight: "0.5rem",
              }}
            >
              Yes, Delete
            </button>

            <button
              type="button"
              onClick={() => setConfirmDeleteRestaurant(false)}
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    )}

    {restaurantResponse?.deleted && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Restaurant deleted successfully.</p>
        <p>ID: {restaurantResponse.id}</p>
      </div>
    )}
  </div>
)}
  </div>
)}
{tab === "favorites" && (
  <div>
    <h2>Favorites</h2>

    {/* Sub-tab button */}
    <div style={{ marginBottom: "1rem" }}>
     <button onClick={() => {
  setFavoriteTab("view");
  loadFavorites(); // ← move it here
}}>
  View Favorites
</button>
 <button
    onClick={() => setFavoriteTab("add")}
    style={{ marginLeft: "0.5rem" }}
  >
    Add Favorite
  </button>
  <button
  onClick={() => {
    setFavoriteTab("delete");
    loadFavorites(); // load list to choose from
  }}
  style={{ marginLeft: "0.5rem" }}
>
  Delete Favorite
</button>
    </div>

    {favoriteTab === "view" && (
      <div>
        {favorites.length === 0 ? (
          <p>No favorites yet.</p>
        ) : (
          favorites.map((fav) => (
            <div key={fav.id}>
              <p>ID: {fav.id}</p>
              <p>Restaurant: {fav.restaurant_name}</p>
              <p>Menu Item: {fav.menu_item_name}</p>
            </div>
          ))
        )}
      </div>
    )}

    {favoriteTab === "add" && (
  <div>
    <form onSubmit={handleAddFavorite}>
      <div>
        <input
          placeholder="Restaurant ID"
          value={favoriteForm.restaurant_id}
          onChange={(e) =>
            setFavoriteForm({
              ...favoriteForm,
              restaurant_id: e.target.value,
            })
          }
        />
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <input
          placeholder="Menu Item ID"
          value={favoriteForm.menu_item_id}
          onChange={(e) =>
            setFavoriteForm({
              ...favoriteForm,
              menu_item_id: e.target.value,
            })
          }
        />
      </div>

      <button type="submit" style={{ marginTop: "1rem" }}>
        Add Favorite
      </button>
    </form>
  </div>
)}
{favoriteTab === "delete" && (
  <div>
    <h3>Delete Favorite</h3>

    {favorites.length === 0 ? (
      <p>No favorites to delete.</p>
    ) : (
      favorites.map((fav) => (
        <div
          key={fav.id}
          style={{
            border: "1px solid #ccc",
            padding: "0.5rem",
            marginTop: "0.5rem",
          }}
        >
          <p>ID: {fav.id}</p>
          <p>Restaurant: {fav.restaurant_name}</p>
          <p>Menu Item: {fav.menu_item_name}</p>

          <button
            onClick={() => handleDeleteFavorite(fav.id)}
            style={{
              backgroundColor: "red",
              color: "white",
              marginTop: "0.5rem",
            }}
          >
            Delete
          </button>
        </div>
      ))
    )}
  </div>
)}
  </div>
)}

      {tab === "browse" && user.role === "customer" && (
        <div>
          <h2>Browse Restaurants</h2>

          <form
            onSubmit={(e) => {
            e.preventDefault();
            setSelectedBrowseRestaurant(null);
            loadBrowseRestaurants(1);
          }}
            style={{ marginBottom: "1rem" }}
          >
            <div>
              <input
                placeholder="Search by restaurant name"
                value={browseSearch}
                onChange={(e) => setBrowseSearch(e.target.value)}
              />
            </div>

            <div style={{ marginTop: "0.5rem" }}>
              <input
                placeholder="Tags (comma separated)"
                value={browseTagsInput}
                onChange={(e) => setBrowseTagsInput(e.target.value)}
              />
            </div>

            <button type="submit" style={{ marginTop: "1rem" }}>
              Search
            </button>

            <button
              type="button"
              style={{ marginTop: "1rem", marginLeft: "0.5rem" }}
              onClick={() => {
              setBrowseSearch("");
              setBrowseTagsInput("");
              setSelectedBrowseRestaurant(null);
              setBrowseData({
                items: [],
                total: 0,
                page: 1,
                size: 50,
                pages: 1,
              });
              loadBrowseRestaurants(1);
            }}
            >
              Clear Filters
            </button>
          </form>

          {browseLoading ? (
            <p>Loading restaurants...</p>
          ) : browseData.items.length === 0 ? (
            <p>No restaurants found.</p>
          ) : (
            <div>
              <p>
                Showing page {browseData.page} of {browseData.pages} ({browseData.total} total)
              </p>

              {browseData.items.map((restaurant) => (
                <div
                  key={restaurant.id}
                  onClick={() => loadBrowseRestaurantDetails(restaurant.id)}
                  style={{
                    border: "1px solid #ccc",
                    padding: "1rem",
                    marginTop: "0.75rem",
                    cursor: "pointer",
                  }}
                >
                  <p><strong>ID:</strong> {restaurant.id}</p>
                  <p><strong>Name:</strong> {restaurant.name}</p>
                  <p><strong>Address:</strong> {restaurant.address}</p>
                  <p><strong>Today's Hours:</strong> {restaurant.todays_hours}</p>
                  <p><strong>Tags:</strong> {(restaurant.tags || []).join(", ")}</p>
                  <p>
                    <strong>Average Rating:</strong>{" "}
                    {restaurant.average_rating ?? "No ratings yet"}
                  </p>
                  <p style={{ marginTop: "0.5rem", color: "blue" }}>
                    Click to view full restaurant details
                  </p>
                </div>
              ))}

              <div style={{ marginTop: "1rem" }}>
                <button
                  type="button"
                  disabled={browseData.page <= 1}
                  onClick={() => loadBrowseRestaurants(browseData.page - 1)}
                >
                  Previous
                </button>

                <button
                  type="button"
                  style={{ marginLeft: "0.5rem" }}
                  disabled={browseData.page >= browseData.pages}
                  onClick={() => loadBrowseRestaurants(browseData.page + 1)}
                >
                  Next
                </button>
              </div>
            </div>
          )}

                    {browseDetailLoading && (
            <p style={{ marginTop: "1rem" }}>Loading restaurant details...</p>
          )}

          {selectedBrowseRestaurant && !browseDetailLoading && (
            <div
              style={{
                marginTop: "1.5rem",
                border: "2px solid #999",
                padding: "1rem",
              }}
            >
              <h3>Restaurant Details</h3>

              <p><strong>ID:</strong> {selectedBrowseRestaurant.id}</p>
              <p><strong>Owner User ID:</strong> {selectedBrowseRestaurant.user_id}</p>
              <p><strong>Name:</strong> {selectedBrowseRestaurant.name}</p>
              <p><strong>Phone:</strong> {selectedBrowseRestaurant.phone_number}</p>
              <p><strong>Address:</strong> {selectedBrowseRestaurant.address}</p>
              <p><strong>Tags:</strong> {(selectedBrowseRestaurant.tags || []).join(", ")}</p>
              <p>
                <strong>Average Rating:</strong>{" "}
                {selectedBrowseRestaurant.average_rating ?? "No ratings yet"}
              </p>

                  {/* === ADD THIS inside the selectedBrowseRestaurant details block === */}
    <h4 style={{ marginTop: "1rem" }}>Leave a Rating</h4>

    <form onSubmit={handleAddRating}>
      <div>
        <select
          value={ratingForm.rating}
          onChange={(e) =>
            setRatingForm((prev) => ({
              ...prev,
              rating: e.target.value,
            }))
          }
        >
          <option value="0.5">0.5</option>
          <option value="1.0">1.0</option>
          <option value="1.5">1.5</option>
          <option value="2.0">2.0</option>
          <option value="2.5">2.5</option>
          <option value="3.0">3.0</option>
          <option value="3.5">3.5</option>
          <option value="4.0">4.0</option>
          <option value="4.5">4.5</option>
          <option value="5.0">5.0</option>
        </select>
      </div>

      <div style={{ marginTop: "0.5rem" }}>
        <textarea
          placeholder="Write your review"
          value={ratingForm.review}
          onChange={(e) =>
            setRatingForm((prev) => ({
              ...prev,
              review: e.target.value,
            }))
          }
          rows={4}
          style={{ width: "100%", maxWidth: "500px" }}
        />
      </div>

      <button type="submit" style={{ marginTop: "1rem" }} disabled={ratingLoading}>
        {ratingLoading ? "Submitting Rating..." : "Submit Rating"}
      </button>
    </form>

    {ratingResponse && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Rating submitted successfully.</p>
        <p><strong>Rating ID:</strong> {ratingResponse.id}</p>
        <p><strong>Customer ID:</strong> {ratingResponse.customer_id}</p>
        <p><strong>Rating:</strong> {ratingResponse.rating}</p>
        <p><strong>Review:</strong> {ratingResponse.review}</p>
      </div>
    )}
              <h4 style={{ marginTop: "1rem" }}>Hours</h4>
              {Object.entries(selectedBrowseRestaurant.hours || {}).map(([day, value]) => (
                <p key={day}>
                  <strong>{day}:</strong> {value}
                </p>
              ))}

              <h4 style={{ marginTop: "1rem" }}>Browse Menu</h4>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  loadBrowseRestaurantMenu(selectedBrowseRestaurant.id, 1);
                }}
                style={{ marginBottom: "1rem" }}
              >
                <div>
                  <input
                    placeholder="Search menu items"
                    value={browseMenuSearch}
                    onChange={(e) => setBrowseMenuSearch(e.target.value)}
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <input
                    placeholder="Min price"
                    type="number"
                    min="0"
                    step="0.01"
                    value={browseMenuPriceMin}
                    onChange={(e) => setBrowseMenuPriceMin(e.target.value)}
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <input
                    placeholder="Max price"
                    type="number"
                    min="0"
                    step="0.01"
                    value={browseMenuPriceMax}
                    onChange={(e) => setBrowseMenuPriceMax(e.target.value)}
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <input
                    placeholder="Menu tags (comma separated)"
                    value={browseMenuTagsInput}
                    onChange={(e) => setBrowseMenuTagsInput(e.target.value)}
                  />
                </div>

                <button type="submit" style={{ marginTop: "1rem" }}>
                  Filter Menu
                </button>

                <button
                  type="button"
                  style={{ marginTop: "1rem", marginLeft: "0.5rem" }}
                  onClick={() => {
                    setBrowseMenuSearch("");
                    setBrowseMenuTagsInput("");
                    setBrowseMenuPriceMin("");
                    setBrowseMenuPriceMax("");
                    setBrowseMenuData({
                      items: [],
                      total: 0,
                      page: 1,
                      size: 50,
                      pages: 1,
                    });
                    setTimeout(() => loadBrowseRestaurantMenu(selectedBrowseRestaurant.id, 1), 0);
                  }}
                >
                  Clear Menu Filters
                </button>
              </form>

    <h4 style={{ marginTop: "1rem" }}>Menu</h4>

    {browseMenuLoading ? (
      <p>Loading menu...</p>
    ) : browseMenuData.items.length > 0 ? (
      <div>
        <p>
          Showing menu page {browseMenuData.page} of {browseMenuData.pages} ({browseMenuData.total} total)
        </p>

        {browseMenuData.items.map((item) => (
          <div
            key={item.id}
            style={{
              border: "1px solid #ccc",
              padding: "0.75rem",
              marginTop: "0.5rem",
            }}
          >
            <p><strong>ID:</strong> {item.id}</p>
            <p><strong>Name:</strong> {item.name}</p>
            <p><strong>Price:</strong> {item.price}</p>
            <p><strong>Description:</strong> {item.description}</p>
            <p><strong>Status:</strong> {item.status}</p>
            <p><strong>Tags:</strong> {(item.tags || []).join(", ")}</p>

            <button
              type="button"
              disabled={
                addToCartLoading ||
                !cartResponse ||
                String(cartResponse.restaurant_id) !== String(selectedBrowseRestaurant.id)
              }
              onClick={() => handleAddItemToCart(item)}
              style={{ marginTop: "0.5rem" }}
            >
              Add To Cart
            </button>

            {!cartResponse ||
            String(cartResponse.restaurant_id) !== String(selectedBrowseRestaurant.id) ? (
              <p style={{ marginTop: "0.5rem", color: "gray" }}>
                Start a cart first before adding items.
              </p>
            ) : null}
          </div>
        ))}

        <div style={{ marginTop: "1rem" }}>
          <button
            type="button"
            disabled={browseMenuData.page <= 1}
            onClick={() =>
              loadBrowseRestaurantMenu(
                selectedBrowseRestaurant.id,
                browseMenuData.page - 1
              )
            }
          >
            Previous Menu Page
          </button>

          <button
            type="button"
            style={{ marginLeft: "0.5rem" }}
            disabled={browseMenuData.page >= browseMenuData.pages}
            onClick={() =>
              loadBrowseRestaurantMenu(
                selectedBrowseRestaurant.id,
                browseMenuData.page + 1
              )
            }
          >
            Next Menu Page
          </button>
        </div>
      </div>
    ) : (
      <p>No menu items found.</p>
    )}

               <h4 style={{ marginTop: "1rem" }}>Ratings</h4>
    {selectedBrowseRestaurant.ratings?.length > 0 ? (
      selectedBrowseRestaurant.ratings.map((rating) => (
        <div
          key={rating.id}
          style={{
            border: "1px solid #ccc",
            padding: "0.75rem",
            marginTop: "0.5rem",
          }}
        >
          <p><strong>ID:</strong> {rating.id}</p>
          <p><strong>Customer ID:</strong> {rating.customer_id}</p>
          <p><strong>Rating:</strong> {rating.rating}</p>
          <p><strong>Review:</strong> {rating.review}</p>
        </div>
      ))
    ) : (
      <p>No ratings yet.</p>
    )}
            </div>
          )}

             <div style={{ marginTop: "1rem" }}>
      <button
        type="button"
        onClick={() => handleStartCart(selectedBrowseRestaurant.id)}
        disabled={cartLoading}
      >
        {cartLoading ? "Starting Cart..." : "Start Cart"}
      </button>
    </div>

    {cartResponse && String(cartResponse.restaurant_id) === String(selectedBrowseRestaurant.id) && (
      <div style={{ marginTop: "1rem", color: "green" }}>
        <p>Cart started successfully.</p>
        <p><strong>Cart ID:</strong> {cartResponse.id}</p>
        <p><strong>User ID:</strong> {cartResponse.user_id}</p>
        <p><strong>Restaurant ID:</strong> {cartResponse.restaurant_id}</p>
        <p><strong>Subtotal:</strong> {cartResponse.subtotal}</p>
        <p><strong>Delivery Fee:</strong> {cartResponse.delivery_fee}</p>
        <p><strong>Tax:</strong> {cartResponse.tax}</p>
        <p><strong>Total:</strong> {cartResponse.total}</p>
        <p><strong>Items in Cart:</strong> {(cartResponse.cart_items || []).length}</p>
      </div>
    )}
    {cartMessage && (
  <p style={{ marginTop: "0.5rem", color: "green" }}>{cartMessage}</p>
)}

{cartResponse && String(cartResponse.restaurant_id) === String(selectedBrowseRestaurant.id) && (
  <div style={{ marginTop: "1rem" }}>
    <h4>Current Cart</h4>
    <p><strong>Cart ID:</strong> {cartResponse.id}</p>
    <p><strong>Subtotal:</strong> {cartResponse.subtotal}</p>
    <p><strong>Delivery Fee:</strong> {cartResponse.delivery_fee}</p>
    <p><strong>Tax:</strong> {cartResponse.tax}</p>
    <p><strong>Total:</strong> {cartResponse.total}</p>

    {(cartResponse.cart_items || []).length > 0 ? (
  cartResponse.cart_items.map((cartItem, index) => (
    <div
      key={cartItem.item?.id || index}
      style={{
        border: "1px solid #ccc",
        padding: "0.5rem",
        marginTop: "0.5rem",
      }}
    >
      <p><strong>Name:</strong> {cartItem.item?.name}</p>
      <p><strong>Price:</strong> {cartItem.item?.price}</p>
      <p><strong>Quantity:</strong> {cartItem.quantity}</p>
      <p><strong>Menu Item ID:</strong> {cartItem.item?.id}</p>

      <button
        type="button"
        onClick={() => handleRemoveItemFromCart(cartItem.item?.id)}
        disabled={removeFromCartLoading}
        style={{ marginTop: "0.5rem", backgroundColor: "red", color: "white" }}
      >
        {removeFromCartLoading ? "Removing..." : "Remove From Cart"}
      </button>
    </div>
  ))
) : (
  <p>No items in cart yet.</p>
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
