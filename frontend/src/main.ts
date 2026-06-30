import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./index.css";

import axios from "axios";
import { tenantContext } from "./utils/tenant";

axios.defaults.baseURL = import.meta.env.VITE_API_URL || "";

// Configure Axios request interceptor for multi-tenant headers
axios.interceptors.request.use(
  (config) => {
    if (tenantContext.tenantId) {
      config.headers["X-Tenant-ID"] = tenantContext.tenantId;
    }
    if (tenantContext.branchId) {
      config.headers["X-Branch-ID"] = tenantContext.branchId;
    }
    if (tenantContext.outletId) {
      config.headers["X-Outlet-ID"] = tenantContext.outletId;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const app = createApp(App);
app.use(router);
app.mount("#app");
