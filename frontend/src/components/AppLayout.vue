<template>
  <div class="min-h-screen flex w-full bg-background text-foreground font-sans relative overflow-hidden">
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
          <span class="text-sm font-medium text-muted-foreground hidden sm:inline">
            MSME Client Portal
          </span>
        </div>
        
        <div class="flex items-center gap-3">
          <!-- Notification Bell -->
          <button class="relative p-2 rounded-lg hover:bg-muted text-muted-foreground transition-colors focus:outline-none">
            <Bell class="h-4.5 w-4.5" />
            <span class="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-primary" />
          </button>

          <!-- User Widget -->
          <div class="flex items-center gap-2.5">
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
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { Menu, Bell } from "lucide-vue-next";
import AppSidebar from "./AppSidebar.vue";

const isCollapsed = ref(false);

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
