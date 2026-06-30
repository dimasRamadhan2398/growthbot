<template>
  <aside
    :class="[
      'bg-sidebar text-sidebar-foreground flex flex-col border-r border-sidebar-border transition-all duration-300 z-30 shrink-0 h-screen sticky top-0',
      isCollapsed 
        ? 'w-0 md:w-16 -translate-x-full md:translate-x-0 border-r-0 md:border-r' 
        : 'w-64 translate-x-0 fixed md:sticky left-0 top-0 h-screen shadow-2xl md:shadow-none'
    ]"
  >
    <!-- Header -->
    <div class="h-14 flex items-center px-4 border-b border-sidebar-border shrink-0">
      <div class="flex items-center gap-2.5 overflow-hidden">
        <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
          <Zap class="h-5 w-5" />
        </div>
        <div v-if="!isCollapsed" class="flex flex-col">
          <span class="text-sm font-bold text-sidebar-accent-foreground tracking-tight leading-none">
            AutoPilot AI
          </span>
          <span class="text-[11px] text-sidebar-foreground mt-0.5 leading-none">
            Done-With-You Platform
          </span>
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <div class="flex-1 overflow-y-auto py-3">
      <nav class="px-2 space-y-1">
        <router-link
          v-for="item in computedNavItems"
          :key="item.title"
          :to="item.url"
          v-slot="{ isActive }"
          custom
        >
          <a
            @click="$router.push(item.url)"
            :class="[
              'sidebar-nav-item cursor-pointer group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
              isActive
                ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                : 'hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground text-sidebar-foreground'
            ]"
            :title="isCollapsed ? item.title : ''"
          >
            <component :is="item.icon" class="h-4.5 w-4.5 shrink-0" />
            <span v-if="!isCollapsed" class="transition-opacity duration-200">
              {{ item.title }}
            </span>
          </a>
        </router-link>
      </nav>
    </div>

    <!-- Footer -->
    <div class="p-4 border-t border-sidebar-border" v-if="!isCollapsed">
      <p class="text-[10px] text-muted-foreground text-center">
        v1.0.0 · Local Mode
      </p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import {
  LayoutDashboard,
  GraduationCap,
  Store,
  Bot,
  Package,
  Users,
  Gift,
  CreditCard,
  Zap
} from "lucide-vue-next";

defineProps<{
  isCollapsed: boolean;
}>();

const route = useRoute();

const computedNavItems = computed(() => {
  const industry = route.params.industry || "Retail";
  const branch = route.params.branch || "branch_retail_1";
  const outlet = route.params.outlet || "outlet_retail_1";
  const prefix = `/${industry}/${branch}/${outlet}`;

  return [
    { title: "Dashboard", url: `${prefix}`, icon: LayoutDashboard },
    { title: "AI Academy", url: `${prefix}/academy`, icon: GraduationCap },
    { title: "Webstore & POS", url: `${prefix}/webstore`, icon: Store },
    { title: "My AI Agents", url: `${prefix}/agents`, icon: Bot },
    { title: "Pesanan", url: `${prefix}/orders`, icon: Package },
    { title: "Lead CRM", url: `${prefix}/crm`, icon: Users },
    { title: "Referral Hub", url: `${prefix}/referrals`, icon: Gift },
    { title: "Billing & Usage", url: `${prefix}/billing`, icon: CreditCard },
  ];
});
</script>
