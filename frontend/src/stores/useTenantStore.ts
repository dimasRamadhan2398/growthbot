import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTenantStore = defineStore('tenant', () => {
  const currentTenantId = ref<string | null>(null);
  const currentIndustry = ref<string | null>(null);
  const currentBranchId = ref<string | null>(null);
  const currentOutletId = ref<string | null>(null);

  function resolveTenantFromUrl() {
    // Expected Subdomain logic for Tenant
    // e.g., brand-a.domain.com -> tenant 'brand-a'
    const hostname = window.location.hostname;
    // Example logic: if localhost, might be hard to test subdomain without hosts file,
    // but in prod it extracts the first part. Let's do a simple split.
    const parts = hostname.split('.');
    if (parts.length >= 3 || (parts.length >= 2 && !hostname.includes('localhost'))) {
        currentTenantId.value = parts[0];
    } else {
        // Fallback for local dev if no subdomain is present
        // Or could be extracted from path if desired, but user said "use subdomain using tenant name"
        currentTenantId.value = "myfriedchicken"; // fallback default
    }

    // Expected URL path: https://(subdomain)/FnB/east-jakarta/outlet-east-1
    // Let's parse the pathname
    const pathname = window.location.pathname;
    const pathSegments = pathname.split('/').filter(p => p);

    // According to router setup later, the paths will be prefixed by /:industry/:branchId/:outletId
    // so pathSegments[0] = industry, pathSegments[1] = branchId, pathSegments[2] = outletId
    if (pathSegments.length >= 3 && !['store', 'track', 'api'].includes(pathSegments[0])) {
      currentIndustry.value = pathSegments[0];
      currentBranchId.value = pathSegments[1];
      currentOutletId.value = pathSegments[2];
    } else {
      // Fallback
      currentIndustry.value = "FnB";
      currentBranchId.value = "east-jakarta";
      currentOutletId.value = "outlet-east-1";
    }
  }

  return {
    currentTenantId,
    currentIndustry,
    currentBranchId,
    currentOutletId,
    resolveTenantFromUrl
  };
});
