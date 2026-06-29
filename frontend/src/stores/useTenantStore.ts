import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

export const useTenantStore = defineStore('tenant', () => {
  const currentTenantId = ref<string | null>(null);
  const currentIndustry = ref<string | null>(null);
  const currentBranchId = ref<string | null>(null);
  const currentOutletId = ref<string | null>(null);
  const isReady = ref<boolean>(false);

  async function resolveTenantFromUrl() {
    // Expected Subdomain logic for Tenant
    // e.g., brand-a.domain.com -> tenant 'brand-a'
    const hostname = window.location.hostname;
    // Example logic: if localhost, might be hard to test subdomain without hosts file,
    // but in prod it extracts the first part. Let's do a simple split.
    const parts = hostname.split('.');
    let subdomainCandidate: string | null = null;

    if (parts.length >= 3 || (parts.length >= 2 && !hostname.includes('localhost'))) {
        subdomainCandidate = parts[0];
    }

    if (subdomainCandidate) {
        try {
            // Validate the subdomain against the backend
            const response = await axios.get(`/api/tenants/validate/${subdomainCandidate}`);
            currentTenantId.value = response.data.id;
        } catch (error) {
            console.warn(`Subdomain '${subdomainCandidate}' not found. Using fallback tenant.`);
            currentTenantId.value = "myfriedchicken"; // fallback default
        }
    } else {
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

    isReady.value = true;
  }

  return {
    currentTenantId,
    currentIndustry,
    currentBranchId,
    currentOutletId,
    isReady,
    resolveTenantFromUrl
  };
});
