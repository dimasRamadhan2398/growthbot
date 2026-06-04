<template>
  <div class="min-h-screen bg-background text-foreground font-sans antialiased">
    <!-- Header -->
    <header class="sticky top-0 z-40 bg-card/95 backdrop-blur-md border-b">
      <div class="max-w-3xl mx-auto px-4 h-14 flex items-center gap-3">
        <button @click="backToPortal" class="p-2 -ml-2 rounded-lg hover:bg-muted text-muted-foreground focus:outline-none">
          <ArrowLeft class="h-4.5 w-4.5" />
        </button>
        <h1 class="font-bold text-sm flex-1 text-left">Lacak Pesanan</h1>
        <Package class="h-4.5 w-4.5 text-muted-foreground" />
      </div>
    </header>

    <div class="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <!-- Search Panel -->
      <div class="text-center space-y-4">
        <div class="mx-auto h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20 shadow-sm text-primary">
          <Truck class="h-8 w-8" />
        </div>
        <div>
          <h2 class="text-xl font-bold text-foreground">Lacak Pesanan Anda</h2>
          <p class="text-xs sm:text-sm text-muted-foreground mt-1">Masukkan nomor order atau nomor resi untuk melacak pesanan</p>
        </div>
        <div class="flex gap-2 max-w-md mx-auto">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="ORD-XXXXXXXXXX atau nomor resi..."
              v-model="query"
              @keydown.enter="trackOrder"
              class="pl-9 h-11 w-full bg-card border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
            />
          </div>
          <button @click="trackOrder" class="h-11 px-6 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm">
            Lacak
          </button>
        </div>
        <div class="flex gap-2 justify-center text-[10px] text-muted-foreground">
          <span>Contoh:</span>
          <button 
            v-for="ex in ['ORD-2026041301', 'JNE-1234567890']"
            :key="ex"
            @click="query = ex; trackOrder()"
            class="font-mono bg-muted border px-2 py-0.5 rounded hover:bg-muted/80 transition-colors"
          >
            {{ ex }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-10">
        <RefreshCw class="h-8 w-8 text-primary animate-spin mx-auto" />
        <p class="text-xs text-muted-foreground mt-2">Mencari pesanan...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="searched && !order" class="bg-card border rounded-2xl p-8 text-center animate-fade-in shadow-sm">
        <AlertCircle class="h-12 w-12 mx-auto text-muted-foreground/50 mb-3 animate-pulse" />
        <h3 class="font-bold text-base text-foreground mb-1">Pesanan Tidak Ditemukan</h3>
        <p class="text-xs sm:text-sm text-muted-foreground">Periksa kembali nomor order atau nomor resi Anda.</p>
      </div>

      <!-- Order Details -->
      <div v-else-if="order" class="space-y-4 animate-fade-in text-left">
        
        <!-- Status Banner -->
        <div 
          :class="[
            'bg-card border-2 rounded-2xl p-5 shadow-sm transition-colors duration-300',
            order.status === 'delivered' ? 'border-emerald-500/20' : order.status === 'cancelled' ? 'border-rose-500/20' : 'border-primary/20'
          ]"
        >
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div :class="['p-3 rounded-xl', statusConfig[order.status]?.bgColor || 'bg-muted/20']">
                <component :is="statusIcon(order.status)" class="h-6 w-6 text-primary" :class="statusConfig[order.status]?.color" />
              </div>
              <div>
                <span :class="['px-2.5 py-0.5 rounded-full text-[10px] font-bold border leading-none mb-1 inline-block', statusConfig[order.status]?.bgColor]">
                  {{ statusConfig[order.status]?.label || order.status }}
                </span>
                <p class="text-xs sm:text-sm text-muted-foreground mt-1">
                  {{ order.status === 'delivered' ? 'Pesanan telah diterima' : `Estimasi tiba: ${order.estimated_delivery}` }}
                </p>
              </div>
            </div>
            <div class="text-left sm:text-right shrink-0">
              <p class="text-xs text-muted-foreground">Order ID</p>
              <p class="font-mono font-bold text-sm text-foreground">{{ order.id }}</p>
            </div>
          </div>
        </div>

        <!-- Progress Steps timeline horizontal -->
        <div v-if="order.status !== 'cancelled'" class="bg-card border rounded-2xl p-5 shadow-sm overflow-x-auto">
          <div class="flex items-center justify-between min-w-[500px] pb-2">
            <div v-for="(stepKey, i) in stepOrder" :key="stepKey" class="flex items-center flex-1 last:flex-none">
              <div class="flex flex-col items-center gap-1 min-w-[54px]">
                <div 
                  :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold transition-all',
                    i === currentStepIndex ? 'bg-primary text-primary-foreground ring-4 ring-primary/20' :
                    i < currentStepIndex ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground border'
                  ]"
                >
                  {{ i < currentStepIndex ? "✓" : i + 1 }}
                </div>
                <span :class="['text-[9px] text-center font-bold leading-tight mt-1', i === currentStepIndex ? 'text-primary' : 'text-muted-foreground']">
                  {{ statusConfig[stepKey]?.label.split(" ").slice(0, 2).join(" ") }}
                </span>
              </div>
              <div v-if="i < stepOrder.length - 1" :class="['flex-1 h-0.5 mx-1 rounded', i < currentStepIndex ? 'bg-primary' : 'bg-muted']" />
            </div>
          </div>
        </div>

        <!-- Grid sections -->
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <!-- Timeline Events -->
          <div class="lg:col-span-3 bg-card border rounded-2xl p-5 shadow-sm flex flex-col">
            <h3 class="font-bold text-sm sm:text-base text-foreground mb-4 flex items-center gap-2 border-b pb-3">
              <Clock class="h-4.5 w-4.5 text-primary" /> Riwayat Status
            </h3>
            <div class="space-y-0 relative pl-4 border-l border-border/70 ml-2">
              <div 
                v-for="(ev, idx) in reversedEvents" 
                :key="idx" 
                class="relative pb-5 last:pb-0"
              >
                <!-- Bullet indicator -->
                <span 
                  :class="[
                    'absolute -left-[23px] top-1 h-3.5 w-3.5 rounded-full border-2 border-card shrink-0 transition-all',
                    idx === 0 ? 'bg-primary ring-4 ring-primary/10' : 'bg-muted-foreground/30'
                  ]"
                />
                
                <div>
                  <p :class="['text-xs sm:text-sm font-bold', idx === 0 ? 'text-primary' : 'text-foreground']">{{ ev.label }}</p>
                  <p class="text-xs text-muted-foreground mt-0.5 leading-snug">{{ ev.description }}</p>
                  <div class="flex items-center gap-3 mt-1.5 text-[10px] text-muted-foreground">
                    <span>{{ ev.timestamp }}</span>
                    <span v-if="ev.location" class="flex items-center gap-0.5">
                      <MapPin class="h-3 w-3" /> {{ ev.location }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Summary specs -->
          <div class="lg:col-span-2 space-y-4">
            <!-- Delivery Courier Details -->
            <div class="bg-card border rounded-xl p-4 shadow-sm space-y-3">
              <h3 class="font-bold text-xs sm:text-sm text-foreground flex items-center gap-2 border-b pb-2">
                <Truck class="h-4 w-4 text-primary" /> Info Pengiriman
              </h3>
              <div class="space-y-2 text-xs sm:text-sm text-foreground">
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Kurir</span>
                  <span class="font-bold">{{ order.shipping_method }}</span>
                </div>
                <div class="flex justify-between items-center" v-if="order.tracking_number">
                  <span class="text-muted-foreground">No. Resi</span>
                  <div class="flex items-center gap-1">
                    <span class="font-mono font-bold text-xs text-foreground bg-muted px-1.5 py-0.5 rounded border">{{ order.tracking_number }}</span>
                    <button @click="copyTracking" class="p-1 rounded hover:bg-muted transition-colors focus:outline-none border">
                      <component :is="copiedTracking ? Check : Copy" class="h-3 w-3" :class="copiedTracking ? 'text-success' : 'text-muted-foreground'" />
                    </button>
                  </div>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Estimasi Tiba</span>
                  <span class="font-bold">{{ order.estimated_delivery }}</span>
                </div>
              </div>
            </div>

            <!-- Destination Address -->
            <div class="bg-card border rounded-xl p-4 shadow-sm space-y-2.5">
              <h3 class="font-bold text-xs sm:text-sm text-foreground flex items-center gap-2 border-b pb-2">
                <MapPin class="h-4 w-4 text-primary" /> Alamat Tujuan
              </h3>
              <div class="text-xs sm:text-sm text-foreground">
                <p class="font-bold">{{ order.customer_name }}</p>
                <p class="text-[11px] text-muted-foreground mt-0.5">{{ order.customer_phone }}</p>
                <p class="text-muted-foreground text-xs leading-snug mt-1.5">{{ order.address }}</p>
                <p class="text-muted-foreground text-xs leading-none">{{ order.city }}</p>
              </div>
            </div>

            <!-- Payment status -->
            <div class="bg-card border rounded-xl p-4 shadow-sm space-y-2.5">
              <h3 class="font-bold text-xs sm:text-sm text-foreground flex items-center gap-2 border-b pb-2">
                <CreditCard class="h-4 w-4 text-primary" /> Pembayaran
              </h3>
              <div class="space-y-2 text-xs sm:text-sm text-foreground">
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Metode</span>
                  <span class="font-bold">{{ order.payment_method }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-muted-foreground">Status</span>
                  <span 
                    :class="[
                      'inline-flex px-2 py-0.5 rounded-full text-[10px] font-bold border leading-none',
                      order.payment_status === 'paid' 
                        ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' 
                        : 'bg-amber-500/10 text-amber-600 border-amber-500/20'
                    ]"
                  >
                    {{ order.payment_status === 'paid' ? '✓ Lunas' : 'Menunggu' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Product items -->
            <div class="bg-card border rounded-xl p-4 shadow-sm space-y-3">
              <h3 class="font-bold text-xs sm:text-sm text-foreground flex items-center gap-2 border-b pb-2">
                <ShoppingBag class="h-4 w-4 text-primary" /> Rincian Produk
              </h3>
              <div class="divide-y max-h-[180px] overflow-y-auto pr-1 scrollbar-thin">
                <div v-for="(item, idx) in order.items" :key="idx" class="flex items-center gap-2 py-2">
                  <div class="h-9 w-9 rounded-md overflow-hidden bg-muted shrink-0 border">
                    <img :src="getProductImage(item.product_id)" class="h-full w-full object-cover" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-[11px] sm:text-xs font-bold text-foreground truncate leading-snug">{{ getProductName(item.product_id) }}</p>
                    <p class="text-[10px] text-muted-foreground mt-0.5">{{ item.qty }}x {{ formatRp(item.price) }}</p>
                  </div>
                  <span class="text-xs font-bold text-foreground shrink-0">{{ formatRp(item.price * item.qty) }}</span>
                </div>
              </div>
              <div class="space-y-1.5 pt-2.5 border-t text-xs sm:text-sm text-foreground">
                <div class="flex justify-between text-muted-foreground"><span>Subtotal</span><span>{{ formatRp(order.subtotal) }}</span></div>
                <div class="flex justify-between text-muted-foreground"><span>Ongkir</span><span>{{ formatRp(order.shipping_cost) }}</span></div>
                <div class="flex justify-between pt-1.5 border-t font-bold"><span>Total Pembayaran</span><span class="text-primary">{{ formatRp(order.total) }}</span></div>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex gap-2">
              <a :href="`https://wa.me/${storeWhatsapp}?text=${encodeURIComponent(`Halo, saya ingin bertanya tentang pesanan dengan Order ID ${order.id}`)}`" target="_blank" class="flex-1">
                <button class="w-full h-10 border rounded-lg hover:bg-muted text-foreground font-semibold text-xs transition-colors flex items-center justify-center gap-1.5 focus:outline-none">
                  <MessageCircle class="h-4 w-4 text-emerald-500" /> Hubungi Penjual
                </button>
              </a>
              <button @click="visitStore" class="flex-1 h-10 border rounded-lg hover:bg-muted text-foreground font-semibold text-xs transition-colors flex items-center justify-center gap-1.5 focus:outline-none">
                <StoreIcon class="h-4 w-4 text-primary" /> Kunjungi Toko
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useSearchParams, useRouter } from "vue-router";
import axios from "axios";
import {
  ArrowLeft,
  Package,
  MapPin,
  Truck,
  Phone,
  Copy,
  Check,
  Clock,
  CheckCircle2,
  AlertCircle,
  CreditCard,
  ShoppingBag,
  MessageCircle,
  Store as StoreIcon,
  RefreshCw
} from "lucide-vue-next";

interface OrderItem {
  product_id: number;
  qty: number;
  price: number;
}

interface TrackingEvent {
  status: string;
  label: string;
  description: string;
  timestamp: string;
  location?: string;
}

interface Order {
  id: string;
  store_name: string;
  store_slug: string;
  customer_name: string;
  customer_phone: string;
  address: string;
  city: string;
  subtotal: number;
  shipping_cost: number;
  total: number;
  shipping_method: string;
  shipping_courier: string;
  tracking_number: string | null;
  payment_method: string;
  payment_status: string;
  status: string;
  estimated_delivery: string;
  created_at: string;
  items: OrderItem[];
  tracking_events: TrackingEvent[];
}

interface Product {
  id: number;
  name: string;
  img: string;
}

const router = useRouter();
const query = ref("");
const searched = ref(false);
const loading = ref(false);
const copiedTracking = ref(false);
const order = ref<Order | null>(null);
const products = ref<Product[]>([]);
const storeWhatsapp = ref("6281234567890");

const stepOrder = [
  "pending_payment", "paid", "processing", "shipped", "in_transit", "out_for_delivery", "delivered"
];

const statusConfig: Record<string, { label: string; color: string; bgColor: string }> = {
  pending_payment: { label: "Menunggu Pembayaran", color: "text-warning", bgColor: "bg-warning/10" },
  paid: { label: "Dibayar", color: "text-info", bgColor: "bg-info/10" },
  processing: { label: "Diproses", color: "text-primary", bgColor: "bg-primary/10" },
  shipped: { label: "Dikirim", color: "text-primary", bgColor: "bg-primary/10" },
  in_transit: { label: "Dalam Perjalanan", color: "text-info", bgColor: "bg-info/10" },
  out_for_delivery: { label: "Sedang Diantar", color: "text-warning", bgColor: "bg-warning/10" },
  delivered: { label: "Terkirim", color: "text-success", bgColor: "bg-success/10" },
  cancelled: { label: "Dibatalkan", color: "text-destructive", bgColor: "bg-destructive/10" },
};

const formatRp = (n: number) => `Rp ${n.toLocaleString("id-ID")}`;

const getProductName = (prodId: number) => {
  const p = products.value.find((pr) => pr.id === prodId);
  return p ? p.name : "Produk";
};

const getProductImage = (prodId: number) => {
  const p = products.value.find((pr) => pr.id === prodId);
  return p ? p.img : "/products/product-kaos.png";
};

const trackOrder = async () => {
  if (!query.value.trim()) return;
  loading.value = true;
  searched.value = true;
  order.value = null;

  try {
    const res = await axios.get(`/api/orders/${query.value.trim()}`);
    order.value = res.data;

    // Load store whatsapp
    if (order.value) {
      const storeRes = await axios.get(`/api/stores/${order.value.store_slug}`);
      storeWhatsapp.value = storeRes.data.whatsapp;
    }
  } catch (error) {
    console.error("Order not found or api failed:", error);
  } finally {
    loading.value = false;
  }
};

const backToPortal = () => {
  router.push("/");
};

const visitStore = () => {
  if (order.value) {
    router.push(`/store/${order.value.store_slug}`);
  }
};

const copyTracking = () => {
  if (order.value?.tracking_number) {
    navigator.clipboard.writeText(order.value.tracking_number);
    copiedTracking.value = true;
    setTimeout(() => {
      copiedTracking.value = false;
    }, 2000);
  }
};

onMounted(async () => {
  // Check search params
  const urlParams = new URLSearchParams(window.location.search);
  const orderId = urlParams.get("id");
  if (orderId) {
    query.value = orderId;
    trackOrder();
  }

  // Load products list for names and images
  try {
    const prodRes = await axios.get("/api/products");
    products.value = prodRes.data;
  } catch (error) {
    console.error(error);
  }
});

const currentStepIndex = computed(() => {
  if (!order.value || order.value.status === "cancelled") return -1;
  return stepOrder.indexOf(order.value.status);
});

const reversedEvents = computed(() => {
  if (!order.value?.tracking_events) return [];
  return [...order.value.tracking_events].reverse();
});

const statusIcon = (status: string) => {
  if (status === "delivered") return CheckCircle2;
  if (status === "cancelled") return AlertCircle;
  if (status === "pending_payment") return CreditCard;
  return Truck;
};
</script>
