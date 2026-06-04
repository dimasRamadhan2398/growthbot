<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p class="text-muted-foreground text-sm mt-1">
          Welcome back, Andi. Here's your AI performance overview.
        </p>
      </div>
      <button 
        @click="fetchData" 
        class="p-2 rounded-lg bg-card border hover:bg-muted text-muted-foreground transition-all flex items-center gap-1.5 text-xs font-semibold"
      >
        <RefreshCw :class="['h-3.5 w-3.5', isLoading ? 'animate-spin' : '']" />
        Sync
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="metric-card animate-pulse h-28 bg-card border"></div>
    </div>

    <!-- Metrics Cards -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="m in metrics" :key="m.label" class="metric-card">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs font-medium text-muted-foreground">{{ m.label }}</p>
            <p class="text-2xl font-bold mt-1">{{ m.value }}</p>
            <span class="inline-flex items-center gap-0.5 text-xs font-medium text-success mt-1">
              <ArrowUpRight class="h-3 w-3" /> {{ m.change }}
            </span>
          </div>
          <div :class="['p-2.5 rounded-lg', m.color]">
            <component :is="iconMap[m.icon]" class="h-5 w-5" />
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Area -->
    <div v-if="!isLoading" class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Area Chart (Messages & Leads) -->
      <div class="lg:col-span-2 bg-card rounded-xl border p-4 flex flex-col justify-between">
        <div class="pb-4">
          <h3 class="text-sm font-semibold">Messages & Leads Over Time</h3>
        </div>
        <div class="relative w-full h-[280px]">
          <!-- SVG Area Chart -->
          <svg viewBox="0 0 600 280" class="w-full h-full">
            <!-- Grid Lines -->
            <line x1="40" y1="40" x2="570" y2="40" stroke="#f1f5f9" stroke-width="1" />
            <line x1="40" y1="100" x2="570" y2="100" stroke="#f1f5f9" stroke-width="1" />
            <line x1="40" y1="160" x2="570" y2="160" stroke="#f1f5f9" stroke-width="1" />
            <line x1="40" y1="220" x2="570" y2="220" stroke="#e2e8f0" stroke-width="1" />

            <!-- Y Axis Labels -->
            <text x="30" y="44" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">6k</text>
            <text x="30" y="104" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">4k</text>
            <text x="30" y="164" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">2k</text>
            <text x="30" y="224" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">0</text>

            <!-- X Axis Labels -->
            <g v-for="(d, idx) in areaData" :key="idx">
              <text :x="getXCoordinate(idx)" y="245" text-anchor="middle" class="text-[11px] fill-muted-foreground font-sans">
                {{ d.month }}
              </text>
              <circle :cx="getXCoordinate(idx)" cy="220" r="2.5" fill="#cbd5e1" />
            </g>

            <!-- Messages Fill & Line (Indigo) -->
            <path :d="messagesAreaPath" fill="url(#colorMessages)" />
            <path :d="messagesLinePath" fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" />

            <!-- Leads Line (Teal - Dashed) -->
            <path :d="leadsLinePath" fill="none" stroke="#14b8a6" stroke-width="2" stroke-dasharray="5,5" stroke-linecap="round" />

            <!-- Data Dots on Hover -->
            <g v-for="(d, idx) in areaData" :key="'dot-' + idx" class="group/dot cursor-pointer">
              <circle 
                :cx="getXCoordinate(idx)" 
                :cy="getMessagesY(d.messages)" 
                r="4" 
                fill="#6366f1" 
                stroke="#fff" 
                stroke-width="1.5"
                class="hover:scale-150 transition-transform" 
              />
              <circle 
                :cx="getXCoordinate(idx)" 
                :cy="getLeadsY(d.leads)" 
                r="4" 
                fill="#14b8a6" 
                stroke="#fff" 
                stroke-width="1.5"
                class="hover:scale-150 transition-transform" 
              />
            </g>

            <!-- Gradients -->
            <defs>
              <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stop-color="#6366f1" stop-opacity="0.2" />
                <stop offset="95%" stop-color="#6366f1" stop-opacity="0" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="flex gap-4 items-center justify-center text-xs pt-2">
          <div class="flex items-center gap-1.5">
            <span class="h-2.5 w-2.5 rounded-full bg-[#6366f1]" />
            <span>Messages automated</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="h-2.5 w-2.5 rounded-full border border-dashed border-[#14b8a6]" />
            <span>Leads qualified</span>
          </div>
        </div>
      </div>

      <!-- Pie Chart (Channels) -->
      <div class="bg-card rounded-xl border p-4 flex flex-col justify-between items-center">
        <div class="w-full pb-2">
          <h3 class="text-sm font-semibold">Channel Distribution</h3>
        </div>
        <div class="relative w-full h-[200px] flex items-center justify-center">
          <svg viewBox="0 0 200 200" class="h-full w-auto">
            <!-- Donut Slices -->
            <g v-for="(slice, i) in donutSlices" :key="slice.channel">
              <circle 
                cx="100" 
                cy="100" 
                r="65" 
                fill="transparent" 
                :stroke="pieColors[i]" 
                stroke-width="24"
                :stroke-dasharray="`${slice.dash} ${408.4 - slice.dash}`"
                :stroke-dashoffset="slice.offset"
                class="hover:opacity-90 transition-opacity cursor-pointer"
              />
            </g>
            <!-- Center Text -->
            <text x="100" y="98" text-anchor="middle" class="text-sm font-bold fill-foreground">Commerce</text>
            <text x="100" y="114" text-anchor="middle" class="text-[10px] font-semibold fill-muted-foreground">Channels</text>
          </svg>
        </div>
        <div class="flex flex-wrap justify-center gap-3 mt-3 w-full">
          <div v-for="(c, i) in channelData" :key="c.channel" class="flex items-center gap-1.5 text-[11px] font-medium">
            <span class="h-2.5 w-2.5 rounded-full" :style="{ backgroundColor: pieColors[i] }" />
            <span>{{ c.channel }} ({{ c.value }}%)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bar Chart (Agent Performance) -->
    <div v-if="!isLoading" class="bg-card rounded-xl border p-4">
      <div class="pb-4">
        <h3 class="text-sm font-semibold">Agent Performance</h3>
      </div>
      <div class="relative w-full h-[240px]">
        <svg viewBox="0 0 600 240" class="w-full h-full">
          <!-- Grid Lines -->
          <line x1="50" y1="30" x2="570" y2="30" stroke="#f1f5f9" stroke-width="1" />
          <line x1="50" y1="80" x2="570" y2="80" stroke="#f1f5f9" stroke-width="1" />
          <line x1="50" y1="130" x2="570" y2="130" stroke="#f1f5f9" stroke-width="1" />
          <line x1="50" y1="180" x2="570" y2="180" stroke="#e2e8f0" stroke-width="1" />

          <!-- Y Axis Labels -->
          <text x="40" y="34" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">1,000</text>
          <text x="40" y="84" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">500</text>
          <text x="40" y="134" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">250</text>
          <text x="40" y="184" text-anchor="end" class="text-[10px] fill-muted-foreground font-mono">0</text>

          <!-- Bars group -->
          <g v-for="(agent, idx) in agentPerformance" :key="agent.name">
            <!-- Conversations Bar (Indigo) -->
            <rect 
              :x="getBarX(idx)" 
              :y="getBarY(agent.conversations)" 
              width="18" 
              :height="getBarHeight(agent.conversations)" 
              fill="#6366f1" 
              rx="3"
              class="hover:opacity-90 transition-all cursor-pointer"
            />
            <!-- Resolved Bar (Teal) -->
            <rect 
              :x="getBarX(idx) + 22" 
              :y="getBarY(agent.resolved)" 
              width="18" 
              :height="getBarHeight(agent.resolved)" 
              fill="#14b8a6" 
              rx="3"
              class="hover:opacity-90 transition-all cursor-pointer"
            />
            <!-- Label -->
            <text :x="getBarX(idx) + 20" y="202" text-anchor="middle" class="text-[11px] fill-muted-foreground font-sans">
              {{ agent.name }}
            </text>
          </g>
        </svg>
      </div>
      <div class="flex gap-4 items-center justify-center text-xs mt-2">
        <div class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-full bg-[#6366f1]" />
          <span>Conversations handled</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-full bg-[#14b8a6]" />
          <span>Resolved queries</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import {
  MessageSquare,
  Clock,
  Bot,
  TrendingUp,
  ArrowUpRight,
  RefreshCw,
  Headphones,
  ShoppingBag,
  HelpCircle,
  Package
} from "lucide-vue-next";

const iconMap = {
  MessageSquare,
  Clock,
  Bot,
  TrendingUp,
  Headphones,
  ShoppingBag,
  HelpCircle,
  Package
};

interface Metric {
  label: string;
  value: string;
  change: string;
  icon: string;
  color: string;
}

interface AreaDataPoint {
  month: string;
  messages: number;
  leads: number;
}

interface ChannelDataPoint {
  channel: string;
  value: number;
}

interface AgentPerformancePoint {
  name: string;
  conversations: number;
  resolved: number;
}

const metrics = ref<Metric[]>([]);
const areaData = ref<AreaDataPoint[]>([]);
const channelData = ref<ChannelDataPoint[]>([]);
const agentPerformance = ref<AgentPerformancePoint[]>([]);
const isLoading = ref(true);

const pieColors = ["#6366f1", "#64748b", "#14b8a6", "#f59e0b"];

const fetchData = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get("/api/dashboard");
    metrics.value = response.data.metrics;
    areaData.value = response.data.areaData;
    channelData.value = response.data.channelData;
    agentPerformance.value = response.data.agentPerformance;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
});

// Area chart coordinate calculations
const getXCoordinate = (index: number) => {
  const marginStart = 50;
  const spacing = 80;
  return marginStart + index * spacing;
};

// Max value is 6000 for Y calculations
const getMessagesY = (value: number) => {
  const yStart = 220; // 0 line
  const maxHeight = 180; // height from 0 to 6000
  return yStart - (value / 6000) * maxHeight;
};

// Max value is 400 for Y calculations (scaled to look nice relative to line height)
const getLeadsY = (value: number) => {
  const yStart = 220;
  const maxHeight = 180;
  return yStart - (value / 400) * maxHeight;
};

const messagesLinePath = computed(() => {
  if (!areaData.value.length) return "";
  return areaData.value.reduce((path, d, idx) => {
    const x = getXCoordinate(idx);
    const y = getMessagesY(d.messages);
    return path + `${idx === 0 ? "M" : "L"}${x},${y}`;
  }, "");
});

const messagesAreaPath = computed(() => {
  if (!areaData.value.length) return "";
  const line = messagesLinePath.value;
  const firstX = getXCoordinate(0);
  const lastX = getXCoordinate(areaData.value.length - 1);
  return `${line} L${lastX},220 L${firstX},220 Z`;
});

const leadsLinePath = computed(() => {
  if (!areaData.value.length) return "";
  return areaData.value.reduce((path, d, idx) => {
    const x = getXCoordinate(idx);
    const y = getLeadsY(d.leads);
    return path + `${idx === 0 ? "M" : "L"}${x},${y}`;
  }, "");
});

// Donut Chart calculations (circumference of R=65 is 2 * PI * 65 = 408.41)
const donutSlices = computed(() => {
  let accumOffset = 0;
  return channelData.value.map((d) => {
    const percent = d.value;
    const dash = (percent / 100) * 408.4;
    const offset = accumOffset;
    accumOffset -= dash;
    return {
      channel: d.channel,
      dash,
      offset
    };
  });
});

// Bar chart calculations (max value is 1000)
const getBarX = (index: number) => {
  const marginStart = 80;
  const spacing = 130;
  return marginStart + index * spacing;
};

const getBarY = (val: number) => {
  const yStart = 180;
  const maxHeight = 150; // height from 0 to 1000
  return yStart - (val / 1000) * maxHeight;
};

const getBarHeight = (val: number) => {
  const maxHeight = 150;
  return (val / 1000) * maxHeight;
};
</script>
