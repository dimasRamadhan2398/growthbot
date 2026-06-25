import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./index.css";

import axios from "axios";
import { useTenantStore } from "./stores/useTenantStore";

axios.defaults.baseURL = import.meta.env.VITE_API_URL || "";

const pinia = createPinia();
const app = createApp(App);

app.use(pinia);

// Resolve tenant and branch immediately upon load
const tenantStore = useTenantStore();
tenantStore.resolveTenantFromUrl();

// Setup Axios Interceptors
axios.interceptors.request.use((config) => {
  if (tenantStore.currentTenantId) {
    config.headers['X-Tenant-ID'] = tenantStore.currentTenantId;
  }
  if (tenantStore.currentBranchId) {
    config.headers['X-Branch-ID'] = tenantStore.currentBranchId;
  }
  if (tenantStore.currentOutletId) {
    config.headers['X-Outlet-ID'] = tenantStore.currentOutletId;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

app.use(router);
app.mount("#app");
