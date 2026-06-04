<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Billing & Usage</h1>
      <p class="text-muted-foreground text-sm mt-1">Manage your subscription and monitor consumption.</p>
    </div>

    <!-- Plans Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div 
        v-for="p in plans" 
        :key="p.name" 
        :class="[
          'bg-card border rounded-xl relative hover:shadow-md transition-shadow flex flex-col justify-between overflow-hidden',
          p.current ? 'border-primary ring-1 ring-primary/20 shadow-sm' : ''
        ]"
      >
        <span 
          v-if="p.current" 
          class="absolute -top-0 right-4 px-2 py-0.5 rounded-b-md bg-primary text-primary-foreground text-[9px] font-bold uppercase tracking-wider shadow-sm"
        >
          Current Plan
        </span>
        <div class="p-5 space-y-4 pt-6">
          <div>
            <h3 class="font-bold text-lg text-foreground">{{ p.name }}</h3>
            <div class="flex items-baseline gap-0.5 mt-1 text-foreground">
              <span class="text-2xl font-extrabold">{{ p.price }}</span>
              <span class="text-xs text-muted-foreground">{{ p.period }}</span>
            </div>
          </div>
          <ul class="space-y-2">
            <li v-for="f in p.features" :key="f" class="flex items-center gap-2 text-xs sm:text-sm text-foreground">
              <Check class="h-4 w-4 text-success shrink-0" />
              {{ f }}
            </li>
          </ul>
        </div>
        <div class="p-5 pt-0">
          <button 
            :disabled="p.current"
            @click="upgradePlan(p.name)"
            :class="[
              'w-full h-9 rounded-lg font-semibold text-xs transition-all outline-none',
              p.current 
                ? 'bg-secondary text-secondary-foreground cursor-default' 
                : 'bg-primary hover:bg-primary/95 text-primary-foreground shadow-sm'
            ]"
          >
            {{ p.current ? "Current Plan" : "Upgrade" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Usage Card -->
    <div class="bg-card border rounded-xl p-5 shadow-sm space-y-5">
      <h3 class="font-bold text-base text-foreground">Usage This Month</h3>
      <div class="space-y-5">
        <div v-for="u in usage" :key="u.label" class="space-y-2">
          <div class="flex justify-between text-xs sm:text-sm">
            <span class="font-semibold text-foreground">{{ u.label }}</span>
            <span class="text-muted-foreground font-mono">{{ formatValue(u.used) }} / {{ formatValue(u.limit) }} {{ u.unit }}</span>
          </div>
          <!-- Custom Progress Bar -->
          <div class="w-full bg-secondary h-2.5 rounded-full overflow-hidden">
            <div class="bg-primary h-full transition-all duration-300" :style="{ width: `${getPercentage(u.used, u.limit)}%` }"></div>
          </div>
          <p class="text-[11px] text-muted-foreground font-medium">{{ getPercentage(u.used, u.limit) }}% used</p>
        </div>
      </div>
    </div>

    <!-- Invoices Card -->
    <div class="bg-card border rounded-xl p-5 shadow-sm space-y-4">
      <h3 class="font-bold text-base text-foreground">Invoice History</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead>
            <tr class="border-b text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <th class="py-3">Date</th>
              <th class="py-3 text-right">Amount</th>
              <th class="py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="inv in invoices" :key="inv.date" class="hover:bg-muted/10 transition-colors">
              <td class="py-3 text-foreground font-medium">{{ inv.date }}</td>
              <td class="py-3 text-right text-foreground font-bold">{{ inv.amount }}</td>
              <td class="py-3 text-center">
                <span class="inline-flex px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20 text-[10px] font-bold">
                  Paid
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Check } from "lucide-vue-next";

const plans = [
  { name: "Starter", price: "Rp 499K", period: "/mo", features: ["3 AI Agents", "5,000 messages/mo", "Basic analytics", "Email support"], current: false },
  { name: "Growth", price: "Rp 1.49M", period: "/mo", features: ["6 AI Agents", "25,000 messages/mo", "Advanced analytics", "Priority support", "POS integration"], current: true },
  { name: "Enterprise", price: "Custom", period: "", features: ["Unlimited agents", "Unlimited messages", "Custom AI training", "Dedicated CSM", "SLA guarantee"], current: false },
];

const usage = [
  { label: "AI Messages", used: 18420, limit: 25000, unit: "messages" },
  { label: "AI Tokens", used: 2100000, limit: 3000000, unit: "tokens" },
  { label: "Knowledge Base Storage", used: 4.2, limit: 10, unit: "GB" },
];

const invoices = [
  { date: "Apr 1, 2026", amount: "Rp 1,490,000", status: "paid" },
  { date: "Mar 1, 2026", amount: "Rp 1,490,000", status: "paid" },
  { date: "Feb 1, 2026", amount: "Rp 1,490,000", status: "paid" },
  { date: "Jan 1, 2026", amount: "Rp 1,290,000", status: "paid" },
];

const getPercentage = (used: number, limit: number) => {
  return Math.round((used / limit) * 100);
};

const formatValue = (val: number) => {
  if (val >= 1000000) return `${(val / 1000000).toFixed(1)}M`;
  if (val >= 1000) return `${(val / 1000).toFixed(1)}K`;
  return val;
};

const upgradePlan = (name: string) => {
  alert(`Initiating upgrade checkout flow for plan: ${name}`);
};
</script>
