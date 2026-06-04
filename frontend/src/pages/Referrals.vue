<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Referral & Partner Hub</h1>
      <p class="text-muted-foreground text-sm mt-1">
        Earn AI credits for every successful referral. Both you and your friend get rewarded.
      </p>
    </div>

    <!-- Referral Link Card -->
    <div class="bg-card border border-primary/20 bg-gradient-to-br from-accent/30 to-background rounded-xl p-5 shadow-sm">
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2.5 rounded-lg bg-primary/10 text-primary">
          <Gift class="h-5 w-5" />
        </div>
        <div>
          <h3 class="font-bold text-sm text-foreground">Two-Sided Rewards</h3>
          <p class="text-xs text-muted-foreground">You get 200 AI credits • Your friend gets 100 AI credits on signup</p>
        </div>
      </div>
      <div class="flex flex-col sm:flex-row gap-2">
        <div class="flex-1 px-4 py-2.5 rounded-lg bg-card border text-sm font-mono truncate text-foreground">
          {{ referralLink }}
        </div>
        <button 
          @click="copyLink" 
          class="h-10 px-5 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm flex items-center justify-center gap-1.5 shrink-0"
        >
          <component :is="copied ? Check : Copy" class="h-4 w-4" />
          {{ copied ? "Copied!" : "Copy Link" }}
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div v-for="s in stats" :key="s.label" class="metric-card">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs font-medium text-muted-foreground">{{ s.label }}</p>
            <p class="text-2xl font-bold mt-1 text-foreground">{{ s.value }}</p>
          </div>
          <div :class="['p-2.5 rounded-lg', s.color]">
            <component :is="s.icon" class="h-5 w-5" />
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Referrals Table -->
    <div class="bg-card border rounded-xl p-5 shadow-sm space-y-4">
      <h3 class="font-bold text-base text-foreground">Recent Referrals</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead>
            <tr class="border-b text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <th class="py-3">Name</th>
              <th class="py-3 text-center">Status</th>
              <th class="py-3 text-right">Reward</th>
              <th class="py-3 text-right">Date</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="r in recentReferrals" :key="r.name + r.date" class="hover:bg-muted/10 transition-colors">
              <td class="py-3 font-semibold text-foreground">{{ r.name }}</td>
              <td class="py-3 text-center">
                <span 
                  :class="[
                    'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold leading-none border',
                    r.status === 'converted' 
                      ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' 
                      : 'bg-slate-500/10 text-slate-500 border-slate-500/20'
                  ]"
                >
                  {{ r.status === "converted" ? "Converted" : "Pending" }}
                </span>
              </td>
              <td class="py-3 text-right font-medium text-foreground">{{ r.reward }}</td>
              <td class="py-3 text-right text-muted-foreground">{{ r.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Gift, MousePointerClick, Users, Zap, Copy, Check } from "lucide-vue-next";

const referralLink = "https://autopilot.ai/ref/ANDI-GR0W7H";
const copied = ref(false);

const stats = [
  { label: "Total Clicks", value: "1,284", icon: MousePointerClick, color: "bg-info/10 text-info" },
  { label: "Successful Referrals", value: "23", icon: Users, color: "bg-success/10 text-success" },
  { label: "Earned AI Credits", value: "4,600", icon: Zap, color: "bg-warning/10 text-warning" },
];

const recentReferrals = [
  { name: "Dewi Lestari", status: "converted", reward: "200 credits", date: "Apr 10, 2026" },
  { name: "Rudi Hermawan", status: "converted", reward: "200 credits", date: "Apr 8, 2026" },
  { name: "Nurul Aini", status: "pending", reward: "—", date: "Apr 7, 2026" },
  { name: "Bambang Suryadi", status: "converted", reward: "200 credits", date: "Apr 3, 2026" },
  { name: "Citra Kirana", status: "pending", reward: "—", date: "Apr 1, 2026" },
];

const copyLink = () => {
  navigator.clipboard.writeText(referralLink);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};
</script>
