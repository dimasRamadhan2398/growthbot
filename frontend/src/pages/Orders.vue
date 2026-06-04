<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Pesanan</h1>
      <p class="text-muted-foreground text-sm mt-1">Kelola semua pesanan dari webstore dan reseller.</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="i in 4" :key="i" class="metric-card animate-pulse h-20 bg-card border"></div>
    </div>

    <!-- Stats Cards -->
    <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="s in stats" :key="s.label" class="metric-card">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs font-medium text-muted-foreground">{{ s.label }}</p>
            <p class="text-xl font-bold mt-1 text-foreground">{{ s.value }}</p>
            <span class="text-[10px] text-muted-foreground leading-none">{{ s.change }}</span>
          </div>
          <div :class="['p-2 rounded-lg', s.color]">
            <component :is="s.icon" class="h-4.5 w-4.5" />
          </div>
        </div>
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="space-y-3">
      <div class="flex gap-2 overflow-x-auto pb-1.5 scrollbar-thin">
        <button
          v-for="tab in filterTabs"
          :key="tab.value"
          @click="selectedFilter = tab.value"
          :class="[
            'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors border focus:outline-none',
            selectedFilter === tab.value
              ? 'bg-primary border-primary text-primary-foreground'
              : 'bg-card border-border text-muted-foreground hover:bg-muted/80'
          ]"
        >
          {{ tab.label }}
          <span 
            :class="[
              'text-[10px] px-1.5 py-0.5 rounded-full font-bold',
              selectedFilter === tab.value ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground border'
            ]"
          >
            {{ getOrdersCountByStatus(tab.value) }}
          </span>
        </button>
      </div>

      <div class="relative max-w-sm">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Cari order ID, nama, atau resi..."
          v-model="searchQuery"
          class="pl-9 h-10 w-full bg-card border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
        />
      </div>
    </div>

    <!-- Orders Table -->
    <div class="bg-card border rounded-xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead>
            <tr class="border-b bg-muted/40 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <th class="py-3.5 px-4">Order ID</th>
              <th class="py-3.5 px-4">Pelanggan</th>
              <th class="py-3.5 px-4">Produk Preview</th>
              <th class="py-3.5 px-4 text-right">Total</th>
              <th class="py-3.5 px-4">Pengiriman</th>
              <th class="py-3.5 px-4 text-center">Status</th>
              <th class="py-3.5 px-4">Tanggal</th>
              <th class="py-3.5 px-4 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="filteredOrders.length === 0">
              <td colspan="8" class="py-12 text-center text-muted-foreground">
                <Package class="h-10 w-10 mx-auto mb-2 opacity-30 animate-bounce" />
                <p class="text-sm font-medium">Tidak ada pesanan ditemukan</p>
              </td>
            </tr>
            <tr v-else v-for="order in filteredOrders" :key="order.id" class="hover:bg-muted/10 transition-colors">
              <td class="py-3.5 px-4">
                <span class="font-mono font-bold text-xs text-foreground">{{ order.id }}</span>
                <p v-if="order.store_name !== 'UrbanStyle Indonesia'" class="text-[10px] text-muted-foreground mt-0.5">
                  via {{ order.store_name }}
                </p>
              </td>
              <td class="py-3.5 px-4">
                <p class="font-bold text-xs text-foreground leading-none">{{ order.customer_name }}</p>
                <p class="text-[10px] text-muted-foreground mt-1">{{ order.city.split(',')[0] }}</p>
              </td>
              <td class="py-3.5 px-4">
                <div class="flex items-center -space-x-2">
                  <div v-for="(item, i) in order.items.slice(0, 3)" :key="i" class="h-7 w-7 rounded-md overflow-hidden border-2 border-card bg-muted shrink-0 shadow-sm">
                    <img :src="getProductImage(item.product_id)" class="h-full w-full object-cover" />
                  </div>
                  <span v-if="order.items.length > 3" class="h-7 w-7 rounded-md bg-muted border-2 border-card flex items-center justify-center text-[9px] font-bold text-muted-foreground shrink-0 shadow-sm">
                    +{{ order.items.length - 3 }}
                  </span>
                </div>
              </td>
              <td class="py-3.5 px-4 text-right font-bold text-foreground text-xs">{{ formatRp(order.total) }}</td>
              <td class="py-3.5 px-4">
                <p class="text-xs text-foreground leading-none">{{ order.shipping_courier }}</p>
                <p v-if="order.tracking_number" class="text-[10px] text-muted-foreground font-mono mt-1">
                  {{ order.tracking_number }}
                </p>
              </td>
              <td class="py-3.5 px-4 text-center">
                <span 
                  :class="[
                    'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border leading-none',
                    statusConfig[order.status]?.bgColor || 'bg-muted/10 text-muted border-border'
                  ]"
                >
                  <component :is="statusIcon(order.status)" class="h-3 w-3 shrink-0" />
                  {{ statusConfig[order.status]?.label || order.status }}
                </span>
              </td>
              <td class="py-3.5 px-4 text-xs text-muted-foreground whitespace-nowrap">
                {{ formatDate(order.created_at) }}
              </td>
              <td class="py-3.5 px-4 text-center">
                <router-link :to="`/track?id=${order.id}`" target="_blank">
                  <button class="p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground focus:outline-none transition-colors border shadow-sm">
                    <Eye class="h-3.5 w-3.5" />
                  </button>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import {
  Package,
  Search,
  Eye,
  Truck,
  Clock,
  CheckCircle2,
  AlertCircle,
  CreditCard,
  ShoppingBag,
  DollarSign
} from "lucide-vue-next";

interface OrderItem {
  id: number;
  product_id: number;
  qty: number;
  price: number;
}

interface Order {
  id: string;
  store_name: string;
  customer_name: string;
  city: string;
  total: number;
  shipping_courier: string;
  tracking_number: string | null;
  status: string;
  created_at: string;
  payment_status: string;
  items: OrderItem[];
}

interface Product {
  id: number;
  name: string;
  img: string;
}

const orders = ref<Order[]>([]);
const products = ref<Product[]>([]);
const isLoading = ref(true);
const selectedFilter = ref("all");
const searchQuery = ref("");

const filterTabs = [
  { label: "Semua", value: "all" },
  { label: "Menunggu Bayar", value: "pending_payment" },
  { label: "Diproses", value: "processing" },
  { label: "Dikirim", value: "shipped,in_transit,out_for_delivery" },
  { label: "Selesai", value: "delivered" },
  { label: "Batal", value: "cancelled" },
];

const statusConfig: Record<string, { label: string; bgColor: string }> = {
  pending_payment: { label: "Menunggu Pembayaran", bgColor: "bg-amber-500/10 text-amber-600 border-amber-500/20" },
  paid: { label: "Dibayar", bgColor: "bg-blue-500/10 text-blue-600 border-blue-500/20" },
  processing: { label: "Diproses", bgColor: "bg-indigo-500/10 text-indigo-600 border-indigo-500/20" },
  shipped: { label: "Dikirim", bgColor: "bg-indigo-500/10 text-indigo-600 border-indigo-500/20" },
  in_transit: { label: "Dalam Perjalanan", bgColor: "bg-blue-500/10 text-blue-600 border-blue-500/20" },
  out_for_delivery: { label: "Sedang Diantar", bgColor: "bg-amber-500/10 text-amber-600 border-amber-500/20" },
  delivered: { label: "Terkirim", bgColor: "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" },
  cancelled: { label: "Dibatalkan", bgColor: "bg-rose-500/10 text-rose-600 border-rose-500/20" },
};

const formatRp = (n: number) => `Rp ${n.toLocaleString("id-ID")}`;

const getProductImage = (prodId: number) => {
  const p = products.value.find((pr) => pr.id === prodId);
  return p ? p.img : "/products/product-kaos.png";
};

const loadData = async () => {
  try {
    const ordersRes = await axios.get("/api/orders");
    orders.value = ordersRes.data;

    const prodRes = await axios.get("/api/products");
    products.value = prodRes.data;
  } catch (error) {
    console.error("Error fetching orders:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadData();
});

const stats = computed(() => {
  const total = orders.value.length;
  const needProcess = orders.value.filter((o) => ["paid", "processing"].includes(o.status)).length;
  const shipping = orders.value.filter((o) => ["shipped", "in_transit", "out_for_delivery"].includes(o.status)).length;
  const revenue = orders.value.filter((o) => o.payment_status === "paid").reduce((s, o) => s + o.total, 0);

  return [
    { label: "Total Pesanan", value: total.toString(), icon: ShoppingBag, color: "bg-primary/10 text-primary", change: "+5 hari ini" },
    { label: "Perlu Diproses", value: needProcess.toString(), icon: Clock, color: "bg-warning/10 text-warning", change: "Action needed" },
    { label: "Dalam Pengiriman", value: shipping.toString(), icon: Truck, color: "bg-info/10 text-info", change: "On track" },
    { label: "Pendapatan Lunas", value: formatRp(revenue), icon: DollarSign, color: "bg-success/10 text-success", change: "+12.5%" },
  ];
});

const getOrdersCountByStatus = (statusFilter: string) => {
  if (statusFilter === "all") return orders.value.length;
  const statuses = statusFilter.split(",");
  return orders.value.filter((o) => statuses.includes(o.status)).length;
};

const filteredOrders = computed(() => {
  return orders.value.filter((o) => {
    const filterStatuses = selectedFilter.value.split(",");
    const matchFilter = selectedFilter.value === "all" || filterStatuses.includes(o.status);
    const matchSearch =
      !searchQuery.value ||
      o.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      o.customer_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (o.tracking_number?.toLowerCase().includes(searchQuery.value.toLowerCase()) ?? false);
    return matchFilter && matchSearch;
  });
});

const statusIcon = (status: string) => {
  if (status === "delivered") return CheckCircle2;
  if (status === "cancelled") return AlertCircle;
  if (status === "pending_payment") return CreditCard;
  return Truck;
};

const formatDate = (isoStr: string) => {
  const d = new Date(isoStr);
  return d.toLocaleDateString("id-ID", { day: "numeric", month: "short" });
};
</script>
