import { useEffect, useRef, useState } from "react";
import {PieChart, Pie, Cell, Tooltip, Legend, LineChart, Line, XAxis, YAxis, BarChart, Bar} from 'recharts';

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
  const [randomMeal, setRandomMeal] = useState(null);
  const [randomMealLoading, setRandomMealLoading] = useState(false);
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

const [orders, setOrders] = useState([]);
const [orderStats, setOrderStats] = useState([]);
const [orderTrend, setOrderTrend] = useState([]);
const [restaurantStats, setRestaurantStats] = useState([]);
const [adminTab, setAdminTab] = useState("analytics");
const [adminRestaurantId, setAdminRestaurantId] = useState("");
const [adminDeleteConfirm, setAdminDeleteConfirm] = useState(false);
const [adminDeleteResponse, setAdminDeleteResponse] = useState(null);
const [adminUserId, setAdminUserId] = useState("");
const [adminUserDeleteConfirm, setAdminUserDeleteConfirm] = useState(false);
const [adminUserDeleteResponse, setAdminUserDeleteResponse] = useState(null);

const [myOrders, setMyOrders] = useState([]);
const [myOrdersLoading, setMyOrdersLoading] = useState(false);
const [placeOrderLoading, setPlaceOrderLoading] = useState(false);
const [placeOrderResponse, setPlaceOrderResponse] = useState(null);
const [selectedPayOrderId, setSelectedPayOrderId] = useState("");
const [paymentForm, setPaymentForm] = useState({
  card_number: "",
  cvv: "",
  expiration_date: "",
});
const [paymentLoading, setPaymentLoading] = useState(false);
const [paymentResponse, setPaymentResponse] = useState(null);

const [restaurantOrders, setRestaurantOrders] = useState([]);
const [restaurantOrdersLoading, setRestaurantOrdersLoading] = useState(false);
const [restaurantOrdersRestaurantId, setRestaurantOrdersRestaurantId] = useState("");
const [restaurantOrderStatusForm, setRestaurantOrderStatusForm] = useState({
  order_id: "",
  status: "Accepted_by_restaurant",
});
const [restaurantOrderStatusResponse, setRestaurantOrderStatusResponse] = useState(null);
const [restaurantOrderStatusLoading, setRestaurantOrderStatusLoading] = useState(false);

const [driverTab, setDriverTab] = useState("available");
const [availableOrders, setAvailableOrders] = useState([]);
const [availableOrdersLoading, setAvailableOrdersLoading] = useState(false);
const [assignedOrders, setAssignedOrders] = useState([]);
const [assignedOrdersLoading, setAssignedOrdersLoading] = useState(false);
const [acceptDeliveryLoading, setAcceptDeliveryLoading] = useState(false);
const [deliveryStatusForm, setDeliveryStatusForm] = useState({
  order_id: "",
  status: "In_transit",
});
const [deliveryStatusLoading, setDeliveryStatusLoading] = useState(false);
const [deliveryStatusResponse, setDeliveryStatusResponse] = useState(null);

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
      if (!user) return;

      const es = new EventSource(
        `http://127.0.0.1:8000/notifications/stream?user_id=${user.user_id}`
      );

      eventSourceRef.current = es;

      es.addEventListener("notification", (event) => {
        const parsed = JSON.parse(event.data);
        setNotifications((prev) => [...prev, parsed]);
      });

      es.onerror = () => {
        console.error("SSE error");
      };

      return () => {
        es.close();
      };
    }, [user]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setResponse("");
    setNotifications([]);

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
  setNotifications([]);
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

const handleGetRandomMeal = async () => {
  if (!user || user.role !== "customer") {
    setError("Only customers can get random meal suggestions");
    return;
  }
  setError("");
  setRandomMeal(null);
  setRandomMealLoading(true);
  try {
    const res = await fetch("http://127.0.0.1:8000/restaurants/random-meal", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });
    const data = await res.json();
    if (!res.ok) {
      let msg = "Failed to get random meal";
      if (typeof data.detail === "string") {
        msg = data.detail;
      } else if (Array.isArray(data.detail)) {
        msg = data.detail.map((x) => x.msg).join(", ");
      } else if (data.detail) {
        msg = JSON.stringify(data.detail);
      }
      throw new Error(msg);
    }
    setRandomMeal(data);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setRandomMealLoading(false);
  }
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

const handlePlaceOrder = async () => {
  if (!user || user.role !== "customer") return;
  if (!cartResponse?.id) return setError("Start a cart for a restaurant first.");
  if ((cartResponse.cart_items || []).length === 0) return setError("Your cart is empty.");

  setError("");
  setPlaceOrderResponse(null);
  setPlaceOrderLoading(true);

  try {
    const res = await fetch("http://127.0.0.1:8000/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
      body: JSON.stringify(cartResponse),
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to place order";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setPlaceOrderResponse(data);
    setCartResponse(null);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setPlaceOrderLoading(false);
  }
};

const loadMyOrders = async () => {
  if (!user) return;
  setError("");
  setMyOrdersLoading(true);

  try {
    const res = await fetch(`http://127.0.0.1:8000/orders`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      if (res.status === 404) { setMyOrders([]); return; }
      let msg = "Failed to load your orders";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setMyOrders(Array.isArray(data) ? data : []);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setMyOrdersLoading(false);
  }
};

const handlePayOrder = async (e) => {
  e.preventDefault();
  if (!user) return;
  if (!selectedPayOrderId.trim()) return setError("Select an order to pay for.");

  setError("");
  setPaymentResponse(null);
  setPaymentLoading(true);

  try {
    const payload = {
      user_id: user.user_id,
      card_number: paymentForm.card_number,
      cvv: paymentForm.cvv,
      expiration_date: paymentForm.expiration_date,
    };

    const res = await fetch(
      `http://127.0.0.1:8000/orders/${selectedPayOrderId}/simulate-payment`,
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
      let msg = "Payment failed";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setPaymentResponse(data);
    setPaymentForm({ card_number: "", cvv: "", expiration_date: "" });
    setSelectedPayOrderId("");
    await loadMyOrders();
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setPaymentLoading(false);
  }
};

const loadRestaurantOrders = async (restaurantId) => {
  if (!user || user.role !== "restaurant_owner") return;
  setError("");
  setRestaurantOrdersLoading(true);

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/orders/restaurant/${restaurantId}/past`,
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
      let msg = "Failed to load restaurant orders";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setRestaurantOrders(Array.isArray(data) ? data : []);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setRestaurantOrdersLoading(false);
  }
};

const handleUpdateRestaurantStatus = async (e) => {
  e.preventDefault();
  if (!user || user.role !== "restaurant_owner") return;
  if (!restaurantOrderStatusForm.order_id.trim()) return setError("Order ID is required.");

  setError("");
  setRestaurantOrderStatusResponse(null);
  setRestaurantOrderStatusLoading(true);

  try {
    const res = await fetch(
    `http://127.0.0.1:8000/orders/${restaurantOrderStatusForm.order_id}/restaurant/${restaurantOrderStatusForm.status}`,
      {
        method: "PATCH",
        headers:  {"Content-Type": "application/json", "user-id": user.user_id },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to update order status";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setRestaurantOrderStatusResponse(data);
    if (restaurantOrdersRestaurantId.trim()) {
      await loadRestaurantOrders(restaurantOrdersRestaurantId);
    }
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setRestaurantOrderStatusLoading(false);
  }
};

const loadAvailableOrders = async () => {
  if (!user || user.role !== "delivery_driver") return;
  setError("");
  setAvailableOrdersLoading(true);

  try {
    const res = await fetch("http://127.0.0.1:8000/orders/available", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to load available orders";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setAvailableOrders(Array.isArray(data) ? data : []);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setAvailableOrdersLoading(false);
  }
};

const handleAcceptDelivery = async (orderId) => {
  if (!user || user.role !== "delivery_driver") return;
  setError("");
  setAcceptDeliveryLoading(true);

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/orders/${orderId}/accept`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to accept delivery";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    await loadAvailableOrders();
    await loadAssignedOrders();
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setAcceptDeliveryLoading(false);
  }
};

const loadAssignedOrders = async () => {
  if (!user || user.role !== "delivery_driver") return;
  setError("");
  setAssignedOrdersLoading(true);

  try {
    const res = await fetch("http://127.0.0.1:8000/orders/assigned", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      if (res.status === 404) { setAssignedOrders([]); return; }
      let msg = "Failed to load assigned orders";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setAssignedOrders(Array.isArray(data) ? data : []);
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setAssignedOrdersLoading(false);
  }
};

const handleUpdateDeliveryStatus = async (e) => {
  e.preventDefault();
  if (!user || user.role !== "delivery_driver") return;
  if (!deliveryStatusForm.order_id.trim()) return setError("Order ID is required.");

  setError("");
  setDeliveryStatusResponse(null);
  setDeliveryStatusLoading(true);

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/orders/${deliveryStatusForm.order_id}/${deliveryStatusForm.status}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    const data = await res.json();

    if (!res.ok) {
      let msg = "Failed to update delivery status";
      if (typeof data.detail === "string") msg = data.detail;
      else if (Array.isArray(data.detail)) msg = data.detail.map((x) => x.msg).join(", ");
      else if (data.detail) msg = JSON.stringify(data.detail);
      throw new Error(msg);
    }

    setDeliveryStatusResponse(data);
    await loadAssignedOrders();
  } catch (err) {
    setError(err.message || "Something went wrong");
  } finally {
    setDeliveryStatusLoading(false);
  }
};

const loadAdminData = async () => {
  setError("");

  try {
    const res = await fetch("http://127.0.0.1:8000/orders", {
      headers: {
        "Content-Type": "application/json",
        "user-id": user.user_id,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error("Failed to load orders");
    }

    setOrders(data);

    const counts = {};

    data.forEach((order) => {
      counts[order.status] = (counts[order.status] || 0) + 1;
    });

    const formatted = Object.entries(counts).map(([status, count]) => ({
      name: status,
      value: count,
    }));

    setOrderStats(formatted);

    const dateCounts = {};

data.forEach((order) => {
  const date = order.order_date;
  dateCounts[date] = (dateCounts[date] || 0) + 1;
});

const trendData = Object.entries(dateCounts)
  .map(([date, count]) => ({
    date,
    count,
  }))
  .sort((a, b) => new Date(a.date) - new Date(b.date));

setOrderTrend(trendData);


  const restaurantCounts = {};

data.forEach((order) => {
  restaurantCounts[order.restaurant_id] =
    (restaurantCounts[order.restaurant_id] || 0) + 1;
});

const restaurantData = Object.entries(restaurantCounts).map(
  ([id, count]) => ({
    restaurant: id,
    orders: count,
  })
);
setRestaurantStats(restaurantData);

  } catch (err) {
    setError(err.message || "Something went wrong");
  }


};

const handleAdminDeleteRestaurant = async () => {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/restaurants/${adminRestaurantId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    if (!res.ok) throw new Error("Delete failed");

    alert("Deleted successfully");
    setAdminRestaurantId("");
    setAdminDeleteConfirm(false);
  } catch (err) {
    setError(err.message);
  }
};

const handleAdminDeleteUser = async () => {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/users/${adminUserId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "user-id": user.user_id,
        },
      }
    );

    if (!res.ok) throw new Error("Delete failed");

    setAdminUserDeleteResponse({ deleted: true, id: adminUserId });
    setAdminUserId("");
    setAdminUserDeleteConfirm(false);
  } catch (err) {
    setError(err.message);
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
                   {user.role === "customer" && (
            <button
              onClick={() => {
                setTab("my-orders");
                setPlaceOrderResponse(null);
                setPaymentResponse(null);
                loadMyOrders();
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              My Orders
            </button>
          )}

          {user.role === "restaurant_owner" && (
            <button
              onClick={() => {
                setTab("manage-orders");
                setRestaurantOrders([]);
                setRestaurantOrderStatusResponse(null);
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              Manage Orders
            </button>
          )}

          {user.role === "delivery_driver" && (
            <button
              onClick={() => {
                setTab("deliveries");
                setDriverTab("available");
                loadAvailableOrders();
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              Deliveries
            </button>
          )}

{user.role === "admin" && (
  <button
    onClick={() => setTab("admin")}
    style={{ marginLeft: "0.5rem" }}
  >
    Dashboard
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
          <p>Welcome to the Food Delivery App!</p>
          {user.role === "customer" && (
            <div style={{ marginTop: "1rem" }}>
              <button
                onClick={handleGetRandomMeal}
                disabled={randomMealLoading}
                style={{
                  padding: "10px 20px",
                  fontSize: "16px",
                  backgroundColor: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: randomMealLoading ? "not-allowed" : "pointer",
                }}
              >
                {randomMealLoading ? "Loading..." : "Get Random Meal 🍽"}
              </button>
              {randomMeal && (
                <div
                  style={{
                    marginTop: "1.5rem",
                    padding: "1rem",
                    border: "2px solid #4CAF50",
                    borderRadius: "8px",
                    backgroundColor: "#f9f9f9",
                  }}
                >
                  <h3>Today's Random Suggestion!</h3>
                  <p><strong>Meal:</strong> {randomMeal.name}</p>
                  <p><strong>Restaurant:</strong> {randomMeal.restaurant_name}</p>
                  <p><strong>Price:</strong> ${randomMeal.price}</p>
                  <p><strong>Description:</strong> {randomMeal.description}</p>
                  <p><strong>Tags:</strong> {(randomMeal.tags || []).join(", ")}</p>
                </div>
              )}
            </div>
          )}
          {user.role !== "customer" && (
            <p style={{ marginTop: "1rem", color: "#666" }}>
              Random meal suggestions are only available for customers.
            </p>
          )}
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
    loadFavorites();
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

      {tab === "my-orders" && user.role === "customer" && (
        <div>
          <h2>My Orders</h2>

          {cartResponse && (cartResponse.cart_items || []).length > 0 && (
            <div style={{ marginBottom: "1.5rem", border: "1px solid #ccc", padding: "1rem" }}>
              <h4>Active Cart</h4>
              <p><strong>Restaurant ID:</strong> {cartResponse.restaurant_id}</p>
              <p><strong>Total:</strong> ${cartResponse.total}</p>
              <p><strong>Items:</strong> {(cartResponse.cart_items || []).length}</p>

              <button
                type="button"
                onClick={handlePlaceOrder}
                disabled={placeOrderLoading}
                style={{ marginTop: "0.5rem" }}
              >
                {placeOrderLoading ? "Placing Order..." : "Place Order"}
              </button>

              {placeOrderResponse && (
                <div style={{ marginTop: "0.5rem", color: "green" }}>
                  <p>Order placed!</p>
                  <p><strong>Order ID:</strong> {placeOrderResponse.id}</p>
                  <p><strong>Status:</strong> {placeOrderResponse.status}</p>
                  <p><strong>Total:</strong> ${placeOrderResponse.order_value}</p>
                </div>
              )}
            </div>
          )}

          <button type="button" onClick={loadMyOrders} style={{ marginBottom: "1rem" }}>
            Refresh Orders
          </button>

          {myOrdersLoading ? (
            <p>Loading orders...</p>
          ) : myOrders.length === 0 ? (
            <p>No orders yet.</p>
          ) : (
            <div>
              {myOrders.map((order) => (
                <div
                  key={order.id}
                  style={{ border: "1px solid #ccc", padding: "0.75rem", marginTop: "0.5rem" }}
                >
                  <p><strong>Order ID:</strong> {order.id}</p>
                  <p><strong>Restaurant ID:</strong> {order.restaurant_id}</p>
                  <p><strong>Items:</strong> {order.food_items}</p>
                  <p><strong>Date:</strong> {order.order_date}</p>
                  <p><strong>Total:</strong> ${order.order_value}</p>
                  <p><strong>Status:</strong> {order.status}</p>

                  {order.status === "Pending" && (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedPayOrderId(order.id);
                        setPaymentResponse(null);
                      }}
                      style={{ marginTop: "0.5rem" }}
                    >
                      Pay for this Order
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {selectedPayOrderId && (
            <div style={{ marginTop: "1.5rem", border: "1px solid #999", padding: "1rem" }}>
              <h4>Pay for Order {selectedPayOrderId}</h4>

              <form onSubmit={handlePayOrder}>
                <div>
                  <input
                    placeholder="Card number (15 or 16 digits)"
                    value={paymentForm.card_number}
                    onChange={(e) =>
                      setPaymentForm({ ...paymentForm, card_number: e.target.value })
                    }
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <input
                    placeholder="CVV"
                    value={paymentForm.cvv}
                    onChange={(e) =>
                      setPaymentForm({ ...paymentForm, cvv: e.target.value })
                    }
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <input
                    placeholder="Expiration date (MM/YY)"
                    value={paymentForm.expiration_date}
                    onChange={(e) =>
                      setPaymentForm({ ...paymentForm, expiration_date: e.target.value })
                    }
                  />
                </div>

                <button
                  type="submit"
                  disabled={paymentLoading}
                  style={{ marginTop: "1rem" }}
                >
                  {paymentLoading ? "Processing..." : "Submit Payment"}
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedPayOrderId("")}
                  style={{ marginLeft: "0.5rem", marginTop: "1rem" }}
                >
                  Cancel
                </button>
              </form>

              {paymentResponse && (
                <p style={{ marginTop: "0.5rem", color: "green" }}>
                  {paymentResponse.message}
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {tab === "manage-orders" && user.role === "restaurant_owner" && (
        <div>
          <h2>Manage Orders</h2>

          <div style={{ marginBottom: "1rem" }}>
            <input
              placeholder="Restaurant ID"
              value={restaurantOrdersRestaurantId}
              onChange={(e) => setRestaurantOrdersRestaurantId(e.target.value)}
            />
            <button
              type="button"
              onClick={() => {
                if (!restaurantOrdersRestaurantId.trim())
                  return setError("Enter a restaurant ID");
                setError("");
                loadRestaurantOrders(restaurantOrdersRestaurantId);
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              Load Orders
            </button>
          </div>

          {restaurantOrdersLoading ? (
            <p>Loading orders...</p>
          ) : restaurantOrders.length === 0 ? (
            <p>No orders found for this restaurant.</p>
          ) : (
            <div>
              {restaurantOrders.map((order) => (
                <div
                  key={order.id}
                  style={{ border: "1px solid #ccc", padding: "0.75rem", marginTop: "0.5rem" }}
                >
                  <p><strong>Order ID:</strong> {order.id}</p>
                  <p><strong>Customer ID:</strong> {order.customer_id}</p>
                  <p><strong>Items:</strong> {order.food_items}</p>
                  <p><strong>Date:</strong> {order.order_date}</p>
                  <p><strong>Total:</strong> ${order.order_value}</p>
                  <p><strong>Status:</strong> {order.status}</p>
                  <p><strong>Driver:</strong> {order.assigned_driver_id || "Unassigned"}</p>
                </div>
              ))}
            </div>
          )}

          <div style={{ marginTop: "1.5rem", border: "1px solid #999", padding: "1rem" }}>
            <h4>Update Order Status</h4>

            <form onSubmit={handleUpdateRestaurantStatus}>
              <div>
                <input
                  placeholder="Order ID"
                  value={restaurantOrderStatusForm.order_id}
                  onChange={(e) =>
                    setRestaurantOrderStatusForm({
                      ...restaurantOrderStatusForm,
                      order_id: e.target.value,
                    })
                  }
                />
              </div>

              <div style={{ marginTop: "0.5rem" }}>
                <select
                  value={restaurantOrderStatusForm.status}
                  onChange={(e) =>
                    setRestaurantOrderStatusForm({
                      ...restaurantOrderStatusForm,
                      status: e.target.value,
                    })
                  }
                >
                  <option value="Accepted_by_restaurant">Accept Order</option>
                  <option value="Preparing">Preparing</option>
                  <option value="Ready_for_pickup">Ready for Pickup</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={restaurantOrderStatusLoading}
                style={{ marginTop: "1rem" }}
              >
                {restaurantOrderStatusLoading ? "Updating..." : "Update Status"}
              </button>
            </form>

            {restaurantOrderStatusResponse && (
              <div style={{ marginTop: "0.5rem", color: "green" }}>
                <p>Status updated!</p>
                <p><strong>Order ID:</strong> {restaurantOrderStatusResponse.id}</p>
                <p><strong>New Status:</strong> {restaurantOrderStatusResponse.status}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {tab === "deliveries" && user.role === "delivery_driver" && (
        <div>
          <h2>Deliveries</h2>

          <div style={{ marginBottom: "1rem" }}>
            <button
              type="button"
              onClick={() => {
                setDriverTab("available");
                loadAvailableOrders();
              }}
            >
              Available Orders
            </button>

            <button
              type="button"
              onClick={() => {
                setDriverTab("assigned");
                loadAssignedOrders();
              }}
              style={{ marginLeft: "0.5rem" }}
            >
              My Deliveries
            </button>

            <button
              type="button"
              onClick={() => setDriverTab("update-status")}
              style={{ marginLeft: "0.5rem" }}
            >
              Update Delivery Status
            </button>
          </div>

          {driverTab === "available" && (
            <div>
              <h4>Available Orders</h4>

              <button
                type="button"
                onClick={loadAvailableOrders}
                style={{ marginBottom: "0.75rem" }}
              >
                Refresh
              </button>

              {availableOrdersLoading ? (
                <p>Loading...</p>
              ) : availableOrders.length === 0 ? (
                <p>No available orders right now.</p>
              ) : (
                availableOrders.map((order) => (
                  <div
                    key={order.id}
                    style={{ border: "1px solid #ccc", padding: "0.75rem", marginTop: "0.5rem" }}
                  >
                    <p><strong>Order ID:</strong> {order.id}</p>
                    <p><strong>Restaurant ID:</strong> {order.restaurant_id}</p>
                    <p><strong>Items:</strong> {order.food_items}</p>
                    <p><strong>Total:</strong> ${order.order_value}</p>
                    <p><strong>Status:</strong> {order.status}</p>

                    <button
                      type="button"
                      onClick={() => handleAcceptDelivery(order.id)}
                      disabled={acceptDeliveryLoading}
                      style={{ marginTop: "0.5rem" }}
                    >
                      {acceptDeliveryLoading ? "Accepting..." : "Accept Delivery"}
                    </button>
                  </div>
                ))
              )}
            </div>
          )}

          {driverTab === "assigned" && (
            <div>
              <h4>My Deliveries</h4>

              <button
                type="button"
                onClick={loadAssignedOrders}
                style={{ marginBottom: "0.75rem" }}
              >
                Refresh
              </button>

              {assignedOrdersLoading ? (
                <p>Loading...</p>
              ) : assignedOrders.length === 0 ? (
                <p>No deliveries assigned to you.</p>
              ) : (
                assignedOrders.map((order) => (
                  <div
                    key={order.id}
                    style={{ border: "1px solid #ccc", padding: "0.75rem", marginTop: "0.5rem" }}
                  >
                    <p><strong>Order ID:</strong> {order.id}</p>
                    <p><strong>Restaurant ID:</strong> {order.restaurant_id}</p>
                    <p><strong>Customer ID:</strong> {order.customer_id}</p>
                    <p><strong>Items:</strong> {order.food_items}</p>
                    <p><strong>Total:</strong> ${order.order_value}</p>
                    <p><strong>Status:</strong> {order.status}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {driverTab === "update-status" && (
            <div>
              <h4>Update Delivery Status</h4>

              <form onSubmit={handleUpdateDeliveryStatus}>
                <div>
                  <input
                    placeholder="Order ID"
                    value={deliveryStatusForm.order_id}
                    onChange={(e) =>
                      setDeliveryStatusForm({
                        ...deliveryStatusForm,
                        order_id: e.target.value,
                      })
                    }
                  />
                </div>

                <div style={{ marginTop: "0.5rem" }}>
                  <select
                    value={deliveryStatusForm.status}
                    onChange={(e) =>
                      setDeliveryStatusForm({
                        ...deliveryStatusForm,
                        status: e.target.value,
                      })
                    }
                  >
                    <option value="In_transit">In Transit</option>
                    <option value="Complete">Complete</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={deliveryStatusLoading}
                  style={{ marginTop: "1rem" }}
                >
                  {deliveryStatusLoading ? "Updating..." : "Update Status"}
                </button>
              </form>

              {deliveryStatusResponse && (
                <div style={{ marginTop: "0.5rem", color: "green" }}>
                  <p>Status updated!</p>
                  <p><strong>Order ID:</strong> {deliveryStatusResponse.id}</p>
                  <p><strong>New Status:</strong> {deliveryStatusResponse.status}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

{tab === "admin" && user.role === "admin" && (
  <div>
    <h2>Admin Dashboard</h2>

<div style={{ marginBottom: "1rem" }}>
  <button
    onClick={() => {
      setAdminTab("analytics");
      loadAdminData();
    }}
  >
    Load Analytics
  </button>

  <button
    onClick={() => setAdminTab("delete-restaurants")}
    style={{ marginLeft: "0.5rem" }}
  >
    Delete Restaurants
  </button>
  <button
    onClick={() => setAdminTab("delete-users")}
    style={{ marginLeft: "0.5rem" }}
  >
    Delete Users
  </button>
</div>
{adminTab === "analytics" && (
    <>
  {orderStats.length === 0 ? (
    <p>No data yet. Click "Load Analytics".</p>
  ) : (
    <div
      style={{
        display: "flex",
        gap: "2rem",
        alignItems: "flex-start",
        flexWrap: "wrap",
      }}
    >

      <div>
        <h4 style={{ textAlign: "center" }}>Order Status Distribution</h4>

        <PieChart width={400} height={400}>
          <Pie
            data={orderStats}
            dataKey="value"
            nameKey="name"
            outerRadius={120}
            label
          >
            {orderStats.map((entry, index) => (
              <Cell
                key={index}
                fill={["#0088FE", "#00C49F", "#FFBB28", "#FF8042"][index % 4]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      <div>
        <h4 style={{ textAlign: "center" }}>Orders Over Time</h4>

        <LineChart width={500} height={300} data={orderTrend}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="count" />
        </LineChart>
      </div>
      <div
  style={{
    padding: "1rem",
    border: "1px solid #444",
    borderRadius: "10px",
    backgroundColor: "#111",
  }}
>
  <h4 style={{ textAlign: "center" }}>Top Restaurants</h4>

  <BarChart width={400} height={300} data={restaurantStats}>
    <XAxis dataKey="restaurant" />
    <YAxis />
    <Tooltip />
    <Legend />
    <Bar dataKey="orders" fill="#8884d8"/>
  </BarChart>
</div>
    </div>
  )}
  </>
  )}

  {adminTab === "delete-restaurants" && (
  <div>
    <h3>Delete Restaurants</h3>

    <input
      type="number"
      placeholder="Restaurant ID"
      value={adminRestaurantId}
      onChange={(e) => setAdminRestaurantId(e.target.value)}
    />

    {!adminDeleteConfirm ? (
      <button
        onClick={() => setAdminDeleteConfirm(true)}
        style={{ marginLeft: "0.5rem", backgroundColor: "red", color: "white" }}
      >
        Delete
      </button>
    ) : (
      <div style={{ marginTop: "0.5rem" }}>
        <p style={{ color: "red" }}>
          Are you sure you want to delete this restaurant?
        </p>

        <button
          onClick={handleAdminDeleteRestaurant}
          style={{ backgroundColor: "red", color: "white", marginRight: "0.5rem" }}
        >
          Yes, Delete
        </button>

        <button onClick={() => setAdminDeleteConfirm(false)}>
          Cancel
        </button>
      </div>
    )}

    {adminDeleteResponse?.deleted && (
      <p style={{ color: "green", marginTop: "0.5rem" }}>
        Restaurant {adminDeleteResponse.id} deleted successfully.
      </p>
    )}
  </div>
)}

{adminTab === "delete-users" && (
  <div>
    <h3>Delete Users</h3>

    <input
      placeholder="User ID"
      value={adminUserId}
      onChange={(e) => setAdminUserId(e.target.value)}
    />

    {!adminUserDeleteConfirm ? (
      <button
        onClick={() => setAdminUserDeleteConfirm(true)}
        style={{ marginLeft: "0.5rem", backgroundColor: "red", color: "white" }}
      >
        Delete
      </button>
    ) : (
      <div style={{ marginTop: "0.5rem" }}>
        <p style={{ color: "red" }}>
          Are you sure you want to delete this user?
        </p>

        <button
          onClick={handleAdminDeleteUser}
          style={{
            backgroundColor: "red",
            color: "white",
            marginRight: "0.5rem",
          }}
        >
          Yes, Delete
        </button>

        <button onClick={() => setAdminUserDeleteConfirm(false)}>
          Cancel
        </button>
      </div>
    )}

    {adminUserDeleteResponse?.deleted && (
      <p style={{ color: "green", marginTop: "0.5rem" }}>
        User {adminUserDeleteResponse.id} deleted successfully.
      </p>
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
            notifications.map((n, i) => (
    <div key={i} style={{ marginBottom: "1rem" }}>
      <p><strong>{n.message}</strong></p>
      <small>{new Date(n.timestamp).toLocaleString()}</small>
    </div>
  ))
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
