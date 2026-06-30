import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "./components/AppLayout.vue";
import { updateTenantContext } from "./utils/tenant";

const routes = [
  {
    path: "/",
    redirect: "/Retail/branch_retail_1/outlet_retail_1"
  },
  {
    path: "/:industry/:branch/:outlet",
    component: AppLayout,
    children: [
      {
        path: "",
        name: "Dashboard",
        component: () => import("./pages/Dashboard.vue"),
      },
      {
        path: "academy",
        name: "Academy",
        component: () => import("./pages/Academy.vue"),
      },
      {
        path: "webstore",
        name: "Webstore",
        component: () => import("./pages/Webstore.vue"),
      },
      {
        path: "agents",
        name: "Agents",
        component: () => import("./pages/Agents.vue"),
      },
      {
        path: "crm",
        name: "LeadCRM",
        component: () => import("./pages/LeadCRM.vue"),
      },
      {
        path: "referrals",
        name: "Referrals",
        component: () => import("./pages/Referrals.vue"),
      },
      {
        path: "billing",
        name: "Billing",
        component: () => import("./pages/Billing.vue"),
      },
      {
        path: "orders",
        name: "Orders",
        component: () => import("./pages/Orders.vue"),
      },
    ],
  },
  {
    path: "/store/:storeName",
    name: "PublicStorefront",
    component: () => import("./pages/PublicStorefront.vue"),
  },
  {
    path: "/store/:storeName/checkout",
    name: "Checkout",
    component: () => import("./pages/Checkout.vue"),
  },
  {
    path: "/track",
    name: "TrackOrder",
    component: () => import("./pages/TrackOrder.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("./pages/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const { industry, branch, outlet } = to.params;
  updateTenantContext({
    industry: Array.isArray(industry) ? industry[0] : industry,
    branch: Array.isArray(branch) ? branch[0] : branch,
    outlet: Array.isArray(outlet) ? outlet[0] : outlet,
  });
  next();
});

export default router;
