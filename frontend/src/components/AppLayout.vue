<template>
  <div :class="['min-h-screen flex w-full bg-background text-foreground font-sans relative overflow-hidden', themeClass]">
    <!-- Mobile Sidebar Backdrop Overlay -->
    <div 
      v-if="!isCollapsed" 
      @click="isCollapsed = true" 
      class="fixed inset-0 bg-slate-950/50 backdrop-blur-xs z-25 md:hidden transition-opacity"
    />

    <!-- Sidebar -->
    <AppSidebar :is-collapsed="isCollapsed" />

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      <!-- Header -->
      <header class="h-14 flex items-center justify-between border-b bg-card px-4 shrink-0 z-20">
        <div class="flex items-center gap-3">
          <button
            @click="toggleSidebar"
            class="p-2 -ml-1 rounded-lg hover:bg-muted text-muted-foreground transition-colors focus:outline-none"
            aria-label="Toggle Sidebar"
          >
            <Menu class="h-5 w-5" />
          </button>
          
          <!-- Context Display -->
          <div class="hidden sm:flex flex-col border-l border-border pl-4 ml-2">
            <span class="text-xs font-bold uppercase tracking-wider text-primary">
              {{ currentTenantName }}
            </span>
            <div class="flex items-center text-xs text-muted-foreground mt-0.5 gap-2">
              <span class="flex items-center gap-1"><MapPin class="h-3 w-3" /> {{ currentBranchName }}</span>
              <span class="w-1 h-1 rounded-full bg-border"></span>
              <span class="flex items-center gap-1"><Store class="h-3 w-3" /> {{ currentOutletName }}</span>
            </div>
          </div>
        </div>
        
        <div class="flex items-center gap-3">
          <!-- Context Switcher (Demo Only) -->
          <div class="relative group">
            <button class="flex items-center gap-2 text-xs font-medium border border-border bg-background hover:bg-muted px-3 py-1.5 rounded-md transition-colors">
              <RefreshCw class="h-3.5 w-3.5 text-muted-foreground" />
              <span class="hidden sm:inline">Switch Context</span>
            </button>
            <div class="absolute right-0 top-full mt-1 w-48 bg-card border border-border rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 py-1">
              <div class="px-3 py-2 text-[10px] uppercase font-bold text-muted-foreground tracking-wider bg-muted/50">Demo Tenants</div>
              <router-link to="/Retail/branch_retail_1/outlet_retail_1" class="block px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
                UrbanStyle (Retail)
              </router-link>
              <router-link to="/FnB/branch_fnb_1/outlet_fnb_1" class="block px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
                Tasty Bites (FnB)
              </router-link>
            </div>
          </div>

          <!-- Notification Bell -->
          <button class="relative p-2 rounded-lg hover:bg-muted text-muted-foreground transition-colors focus:outline-none hidden sm:block">
            <Bell class="h-4.5 w-4.5" />
            <span class="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-primary" />
          </button>

          <!-- User Widget -->
          <div class="flex items-center gap-2.5 ml-2 border-l border-border pl-4">
            <div class="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-semibold shrink-0 shadow-sm">
              AR
            </div>
            <div class="hidden md:flex flex-col text-left">
              <span class="text-sm font-medium leading-none">Andi Rahmawan</span>
              <span class="text-[10px] text-muted-foreground mt-0.5">Growth Plan</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Panel View -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6">
        <router-view :key="$route.fullPath" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { Menu, Bell, MapPin, Store, RefreshCw } from "lucide-vue-next";
import AppSidebar from "./AppSidebar.vue";
import { tenantContext } from "../utils/tenant";

const isCollapsed = ref(false);

const themeClass = computed(() => {
  const ind = tenantContext.industry?.toLowerCase();
  if (ind === "fnb") return "theme-fnb";
  if (ind === "retail") return "theme-retail";
  if (ind === "services") return "theme-services";
  return "theme-retail"; // default fallback
});

// Computed properties for Tenant Display
const currentTenantName = computed(() => {
  if (tenantContext.industry?.toLowerCase() === "fnb") return "Tasty Bites Group";
  return "UrbanStyle Indonesia";
});

const currentBranchName = computed(() => {
  if (tenantContext.industry?.toLowerCase() === "fnb") return "Tasty Bites Sudirman";
  return "UrbanStyle Senopati";
});

const currentOutletName = computed(() => {
  if (tenantContext.industry?.toLowerCase() === "fnb") return "Sudirman Central Kitchen";
  return "Senopati Boutique Store";
});

const checkMobile = () => {
  if (window.innerWidth < 768) {
    isCollapsed.value = true;
  } else {
    isCollapsed.value = false;
  }
};

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

onMounted(() => {
  checkMobile();
  window.addEventListener("resize", checkMobile);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile);
});
</script>
