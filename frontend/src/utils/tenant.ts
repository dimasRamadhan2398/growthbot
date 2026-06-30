import { reactive } from "vue";

export const tenantContext = reactive({
  tenantId: "",
  industry: "",
  branchId: "",
  outletId: ""
});

export function updateTenantContext(params: { industry?: string; branch?: string; outlet?: string }) {
  const hostname = window.location.hostname;
  const parts = hostname.split(".");
  let subdomain = "urbanstyle"; // default fallback
  
  if (parts.length > 1 && hostname !== "localhost" && hostname !== "127.0.0.1") {
    subdomain = parts[0];
  } else {
    // In local development, infer the tenant from the industry parameter
    if (params.industry?.toLowerCase() === "fnb") {
      subdomain = "tastybites";
    } else {
      subdomain = "urbanstyle";
    }
  }
  
  tenantContext.tenantId = subdomain;
  tenantContext.industry = params.industry || "";
  tenantContext.branchId = params.branch || "";
  tenantContext.outletId = params.outlet || "";
}
