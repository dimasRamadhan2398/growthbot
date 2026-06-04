<template>
  <div class="min-h-screen bg-background text-foreground font-sans antialiased">
    <!-- Loading State -->
    <div v-if="isLoading" class="min-h-screen flex flex-col items-center justify-center bg-background p-6">
      <RefreshCw class="h-10 w-10 text-primary animate-spin" />
      <p class="text-sm font-semibold text-muted-foreground mt-3">Loading Storefront...</p>
    </div>

    <!-- Store Not Found -->
    <div v-else-if="!store" class="min-h-screen flex flex-col items-center justify-center bg-background p-6 text-center animate-fade-in">
      <StoreIcon class="h-16 w-16 text-muted-foreground mb-4" />
      <h1 class="text-2xl font-bold mb-2">Toko tidak ditemukan</h1>
      <p class="text-muted-foreground text-sm mb-6 max-w-sm leading-relaxed">
        Link toko yang Anda akses tidak valid atau sudah tidak aktif.
      </p>
      <router-link to="/">
        <button class="h-10 px-5 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm flex items-center gap-1.5 focus:outline-none">
          <ArrowLeft class="h-4 w-4" /> Kembali
        </button>
      </router-link>
    </div>

    <!-- Store Found -->
    <div v-else class="min-h-screen flex flex-col justify-between">
      <!-- ─── HEADER ─── -->
      <header class="sticky top-0 z-40 bg-card/95 backdrop-blur-md border-b">
        <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-xl bg-primary flex items-center justify-center shrink-0 shadow-sm text-primary-foreground">
              <StoreIcon class="h-5 w-5" />
            </div>
            <div class="text-left">
              <h1 class="text-sm font-bold leading-tight text-foreground">{{ store.name }}</h1>
              <p class="text-[11px] text-muted-foreground leading-tight mt-0.5">
                {{ store.is_reseller ? `by ${store.owner}` : "Official Store" }}
              </p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <a :href="`https://wa.me/${store.whatsapp}`" target="_blank" class="h-9 px-3 rounded-lg border hover:bg-muted text-foreground font-semibold text-xs transition-all flex items-center gap-1.5">
              <MessageCircle class="h-4 w-4 text-emerald-500" />
              <span class="hidden sm:inline">Chat Penjual</span>
            </a>
            <button 
              @click="cartOpen = true" 
              class="relative p-2.5 rounded-xl hover:bg-muted transition-colors focus:outline-none"
            >
              <ShoppingCart class="h-5 w-5 text-foreground" />
              <span v-if="cartCount > 0" class="absolute -top-0.5 -right-0.5 h-5 w-5 rounded-full bg-primary text-primary-foreground text-[10px] font-bold flex items-center justify-center shadow-sm">
                {{ cartCount }}
              </span>
            </button>
          </div>
        </div>
      </header>

      <!-- ─── HERO ─── -->
      <section class="bg-gradient-to-br from-primary/5 via-accent/30 to-background border-b">
        <div class="max-w-6xl mx-auto px-4 py-10 text-center space-y-3">
          <span 
            :class="[
              'inline-flex px-2.5 py-0.5 rounded-full text-[10px] font-bold border uppercase tracking-wider',
              store.is_reseller ? 'bg-secondary text-secondary-foreground border-border' : 'bg-primary/10 text-primary border-primary/20'
            ]"
          >
            {{ store.is_reseller ? "Reseller Partner" : "Official Store" }}
          </span>
          <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight text-foreground">{{ store.name }}</h2>
          <p class="text-muted-foreground text-sm max-w-md mx-auto leading-relaxed">
            {{ store.tagline }}
          </p>
        </div>
      </section>

      <!-- ─── SEARCH & FILTERS ─── -->
      <div class="max-w-6xl mx-auto px-4 py-5 space-y-3 w-full">
        <div class="flex flex-col sm:flex-row sm:items-center gap-3">
          <div class="relative flex-1 max-w-md">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Cari produk..."
              v-model="searchQuery"
              class="pl-9 h-10 w-full bg-card border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
            />
          </div>
          <div class="relative shrink-0 w-fit">
            <select v-model="sortBy" class="h-9 pl-8 pr-4 bg-card border rounded-lg text-xs font-semibold focus:outline-none cursor-pointer">
              <option v-for="(lbl, val) in sortLabels" :key="val" :value="val">{{ lbl }}</option>
            </select>
            <ArrowUpDown class="h-3.5 w-3.5 text-muted-foreground absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>
        
        <!-- Category chips -->
        <div class="flex items-center gap-2 flex-wrap">
          <button
            v-for="cat in categoryList"
            :key="cat"
            @click="selectedCategory = cat"
            :class="[
              'px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all focus:outline-none',
              selectedCategory === cat
                ? 'bg-primary text-primary-foreground border-primary shadow-sm'
                : 'bg-card text-muted-foreground border-border hover:bg-accent hover:text-accent-foreground'
            ]"
          >
            {{ cat === "Semua" ? "📦 Semua" : cat === "Tops" ? "👕 Atasan" : cat === "Bottoms" ? "👖 Bawahan" : cat === "Accessories" ? "🎒 Aksesoris" : cat }}
          </button>
        </div>
      </div>

      <!-- ─── PRODUCTS GRID ─── -->
      <div class="max-w-6xl mx-auto px-4 pb-24 flex-1 w-full">
        <div v-if="filteredProducts.length === 0" class="text-center py-16 text-muted-foreground">
          <Search class="h-10 w-10 mx-auto mb-3 opacity-40 animate-pulse" />
          <p class="text-sm font-semibold">Produk tidak ditemukan.</p>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          <div 
            v-for="p in filteredProducts" 
            :key="p.id"
            class="group bg-card border rounded-2xl overflow-hidden hover:shadow-lg transition-all duration-300 flex flex-col justify-between"
          >
            <div 
              class="relative aspect-square overflow-hidden cursor-pointer bg-muted"
              @click="selectedProduct = p"
            >
              <img :src="p.img" :alt="p.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              <span v-if="p.sold > 1000" class="absolute top-2 left-2 px-2 py-0.5 rounded bg-amber-500 text-white text-[9px] font-bold uppercase shadow-sm">
                Best Seller
              </span>
            </div>
            <div class="p-3.5 space-y-1.5 text-left">
              <p class="text-[11px] text-muted-foreground">{{ p.category }}</p>
              <h3 
                class="text-xs sm:text-sm font-bold text-foreground leading-tight line-clamp-1 cursor-pointer hover:text-primary transition-colors"
                @click="selectedProduct = p"
              >
                {{ p.name }}
              </h3>
              <div class="flex items-center gap-1.5 text-[10px] text-muted-foreground">
                <Star class="h-3 w-3 fill-warning text-warning" />
                <span class="font-semibold text-foreground">{{ p.rating }}</span>
                <span>· {{ p.sold.toLocaleString() }} terjual</span>
              </div>
              <div class="flex items-center justify-between pt-1.5">
                <span class="text-sm font-bold text-primary">
                  {{ formatRp(getPrice(p)) }}
                </span>
                <button 
                  @click="addToCart(p)" 
                  class="h-8 w-8 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground flex items-center justify-center transition-all shadow-sm focus:outline-none"
                >
                  <Plus class="h-4.5 w-4.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── PRODUCT DETAIL MODAL ─── -->
      <div v-if="selectedProduct" class="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4">
        <div class="bg-card w-full sm:max-w-lg sm:rounded-2xl rounded-t-2xl max-h-[90vh] overflow-y-auto animate-scale-in">
          <div class="relative aspect-square sm:aspect-video overflow-hidden bg-muted">
            <img :src="selectedProduct.img" :alt="selectedProduct.name" class="w-full h-full object-cover" />
            <button 
              @click="selectedProduct = null" 
              class="absolute top-3 right-3 p-2 rounded-full bg-card/85 backdrop-blur-sm shadow text-muted-foreground hover:text-foreground focus:outline-none"
            >
              <X class="h-4 w-4" />
            </button>
          </div>
          <div class="p-5 space-y-4 text-left">
            <div>
              <span class="inline-flex px-2 py-0.5 rounded bg-secondary text-secondary-foreground text-[10px] font-bold mb-2">
                {{ selectedProduct.category }}
              </span>
              <h2 class="text-lg font-bold text-foreground leading-snug">{{ selectedProduct.name }}</h2>
              <div class="flex items-center gap-2 mt-1.5 text-xs text-muted-foreground">
                <Star class="h-3.5 w-3.5 fill-warning text-warning" />
                <span class="font-bold text-foreground">{{ selectedProduct.rating }}</span>
                <span>· {{ selectedProduct.sold.toLocaleString() }} terjual</span>
              </div>
            </div>
            <p class="text-xl font-bold text-primary">{{ formatRp(getPrice(selectedProduct)) }}</p>
            <p class="text-xs sm:text-sm text-muted-foreground leading-relaxed">{{ selectedProduct.description }}</p>
            
            <div class="flex gap-2 pt-2">
              <button 
                @click="addToCart(selectedProduct); selectedProduct = null; cartOpen = true;" 
                class="flex-1 h-11 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all flex items-center justify-center gap-2 shadow-sm focus:outline-none"
              >
                <ShoppingCart class="h-4.5 w-4.5" /> Tambah ke Keranjang
              </button>
              <a 
                :href="`https://wa.me/${store.whatsapp}?text=${encodeURIComponent(`Halo, saya tertarik dengan produk ${selectedProduct.name} (${formatRp(getPrice(selectedProduct))}). Apakah masih tersedia?`)}`"
                target="_blank"
                class="h-11 px-4 border rounded-xl hover:bg-muted text-foreground font-semibold text-sm transition-all flex items-center justify-center gap-2 focus:outline-none"
              >
                <MessageCircle class="h-4.5 w-4.5 text-emerald-500" /> Tanya
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── CART DRAWER ─── -->
      <div v-if="cartOpen" class="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm flex justify-end">
        <div class="bg-card w-full max-w-md h-full flex flex-col animate-slide-in-right shadow-2xl">
          <div class="flex items-center justify-between p-4 border-b">
            <h2 class="font-bold text-base text-foreground flex items-center gap-2">
              <ShoppingCart class="h-5 w-5 text-primary" />
              Keranjang
              <span class="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-xs font-semibold">
                {{ cartCount }}
              </span>
            </h2>
            <button @click="cartOpen = false" class="p-2 rounded-lg hover:bg-muted text-muted-foreground focus:outline-none">
              <X class="h-4.5 w-4.5" />
            </button>
          </div>

          <div class="flex-1 overflow-y-auto divide-y">
            <div v-if="cart.length === 0" class="flex flex-col items-center justify-center h-full text-muted-foreground p-8 text-center space-y-3">
              <ShoppingCart class="h-12 w-12 opacity-30 animate-bounce" />
              <p class="text-sm font-semibold">Keranjang belanja Anda kosong</p>
            </div>
            <div v-for="item in cart" :key="item.id" class="flex items-center gap-3 p-4 hover:bg-muted/10 transition-colors">
              <img :src="item.product.img" :alt="item.product.name" class="h-16 w-16 rounded-xl object-cover shrink-0 bg-muted shadow-sm" />
              <div class="flex-1 min-w-0 text-left">
                <p class="text-sm font-bold text-foreground truncate leading-snug">{{ item.product.name }}</p>
                <p class="text-sm font-bold text-primary mt-1">{{ formatRp(getPrice(item.product)) }}</p>
                <div class="flex items-center gap-1.5 mt-2">
                  <button @click="updateQty(item.id, -1)" class="h-7 w-7 rounded-lg bg-muted hover:bg-muted/80 flex items-center justify-center font-bold text-xs focus:outline-none">-</button>
                  <span class="text-sm font-semibold w-6 text-center">{{ item.qty }}</span>
                  <button @click="updateQty(item.id, 1)" class="h-7 w-7 rounded-lg bg-muted hover:bg-muted/80 flex items-center justify-center font-bold text-xs focus:outline-none">+</button>
                </div>
              </div>
              <div class="text-right flex flex-col justify-between h-[80px] shrink-0">
                <p class="text-sm font-bold text-foreground">{{ formatRp(getPrice(item.product) * item.qty) }}</p>
                <button @click="removeItem(item.id)" class="p-1.5 rounded-md hover:bg-destructive/10 text-destructive self-end focus:outline-none transition-colors">
                  <Trash2 class="h-4.5 w-4.5" />
                </button>
              </div>
            </div>
          </div>

          <div v-if="cart.length > 0" class="border-t p-4 space-y-3 bg-muted/10">
            <div class="flex justify-between text-sm">
              <span class="text-muted-foreground font-medium">Total ({{ cartCount }} item)</span>
              <span class="text-lg font-bold text-primary">{{ formatRp(cartTotal) }}</span>
            </div>
            
            <button 
              @click="proceedToCheckout"
              class="w-full h-12 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-2 focus:outline-none"
            >
              <ShoppingCart class="h-4.5 w-4.5" /> Checkout Sekarang
            </button>
            <button 
              @click="whatsappCheckout"
              class="w-full h-10 rounded-xl bg-card border hover:bg-muted text-foreground font-semibold text-xs transition-all flex items-center justify-center gap-2 focus:outline-none"
            >
              <MessageCircle class="h-4.5 w-4.5 text-emerald-500" /> Checkout via WhatsApp
            </button>

            <div v-if="checkoutDone" class="flex items-center gap-1.5 text-success text-xs font-semibold justify-center animate-fade-in pt-1">
              <CheckCircle class="h-3.5 w-3.5" /> Pesanan dikirim ke WhatsApp!
            </div>
          </div>
        </div>
      </div>

      <!-- ─── FOOTER ─── -->
      <footer class="border-t bg-card py-6">
        <div class="max-w-6xl mx-auto px-4 text-center">
          <p class="text-xs text-muted-foreground">
            {{ store.name }} · Powered by AutoPilot AI
          </p>
        </div>
      </footer>

      <!-- ─── FLOATING CART BUTTON ─── -->
      <button 
        v-if="cartCount > 0 && !cartOpen"
        @click="cartOpen = true"
        class="fixed bottom-6 right-6 z-30 bg-primary hover:bg-primary/90 text-primary-foreground h-14 px-5 rounded-2xl shadow-lg flex items-center gap-2.5 transition-all active:scale-95 animate-scale-in focus:outline-none"
      >
        <ShoppingCart class="h-5 w-5" />
        <span class="font-bold text-sm">{{ formatRp(cartTotal) }}</span>
        <span class="bg-primary-foreground/20 text-primary-foreground text-xs font-bold h-6 w-6 rounded-full flex items-center justify-center">
          {{ cartCount }}
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import {
  Store as StoreIcon,
  ShoppingCart,
  Search,
  Star,
  Plus,
  Minus,
  Trash2,
  X,
  MessageCircle,
  ArrowLeft,
  ArrowUpDown,
  RefreshCw,
  Copy,
  Check,
  CheckCircle,
  ExternalLink
} from "lucide-vue-next";

interface Store {
  slug: string;
  name: string;
  owner: string;
  whatsapp: string;
  tagline: string;
  is_reseller: boolean;
  markup: number;
}

interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock: number;
  rating: number;
  sold: number;
  category: string;
  description: string;
  ch_webstore: boolean;
  img: string;
  status: string;
}

interface CartItem {
  id: number;
  product: Product;
  qty: number;
}

const route = useRoute();
const router = useRouter();
const storeName = route.params.storeName as string;

const store = ref<Store | null>(null);
const products = ref<Product[]>([]);
const isLoading = ref(true);

const searchQuery = ref("");
const selectedCategory = ref("Semua");
const sortBy = ref("default");
const cart = ref<CartItem[]>([]);
const cartOpen = ref(false);
const selectedProduct = ref<Product | null>(null);
const checkoutDone = ref(false);

const sortLabels = {
  default: "Default",
  price_asc: "Harga Terendah",
  price_desc: "Harga Tertinggi",
  bestseller: "Terlaris",
  rating: "Rating Tertinggi",
};

// Retrieve markup price
const getPrice = (p: Product) => {
  if (!store.value) return p.price;
  return Math.round(p.price * (1 + (store.value.markup ?? 0) / 100));
};

const formatRp = (n: number) => `Rp ${n.toLocaleString("id-ID")}`;
const storeUrl = (slug: string) => `${window.location.origin}/store/${slug}`;

const loadStore = async () => {
  try {
    const storeRes = await axios.get(`/api/stores/${storeName}`);
    store.value = storeRes.data;

    const prodRes = await axios.get("/api/products");
    products.value = prodRes.data;

    // Load cart from sessionStorage
    const savedCart = sessionStorage.getItem(`cart_${storeName}`);
    if (savedCart) {
      cart.value = JSON.parse(savedCart);
    }
  } catch (error) {
    console.error("Store not found or products list failed:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadStore();
});

const categoryList = computed(() => {
  const cats = new Set(products.value.map((p) => p.category));
  return ["Semua", ...Array.from(cats)];
});

const categoryLabel = (catId: string) => {
  return catId === "Tops" ? "👕 Atasan" : catId === "Bottoms" ? "👖 Bawahan" : catId === "Accessories" ? "🎒 Aksesoris" : catId;
};

// Filter & Sort
const filteredProducts = computed(() => {
  const list = products.value.filter(
    (p) =>
      p.ch_webstore &&
      p.status !== "out" &&
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
      (selectedCategory.value === "Semua" || p.category === selectedCategory.value)
  );

  const sorted = [...list];
  if (sortBy.value === "price_asc") {
    return sorted.sort((a, b) => getPrice(a) - getPrice(b));
  }
  if (sortBy.value === "price_desc") {
    return sorted.sort((a, b) => getPrice(b) - getPrice(a));
  }
  if (sortBy.value === "bestseller") {
    return sorted.sort((a, b) => b.sold - a.sold);
  }
  if (sortBy.value === "rating") {
    return sorted.sort((a, b) => b.rating - a.rating);
  }
  return sorted;
});

// Cart handlers
const saveCartSession = () => {
  sessionStorage.setItem(`cart_${storeName}`, JSON.stringify(cart.value));
};

const addToCart = (p: Product) => {
  const existing = cart.value.find((i) => i.id === p.id);
  if (existing) {
    existing.qty++;
  } else {
    cart.value.push({
      id: p.id,
      product: p,
      qty: 1
    });
  }
  saveCartSession();
};

const updateQty = (id: number, amt: number) => {
  const item = cart.value.find((i) => i.id === id);
  if (!item) return;
  item.qty += amt;
  if (item.qty <= 0) {
    removeItem(id);
  } else {
    saveCartSession();
  }
};

const removeItem = (id: number) => {
  cart.value = cart.value.filter((i) => i.id !== id);
  saveCartSession();
};

const cartCount = computed(() => cart.value.reduce((s, i) => s + i.qty, 0));
const cartTotal = computed(() => cart.value.reduce((s, i) => s + getPrice(i.product) * i.qty, 0));

// Proceed to checkout
const proceedToCheckout = () => {
  cartOpen.value = false;
  router.push({
    name: "Checkout",
    params: { storeName }
  });
};

const whatsappCheckout = () => {
  if (!store.value) return;
  const itemsText = cart.value
    .map((ci) => `• ${ci.product.name} x${ci.qty} = ${formatRp(getPrice(ci.product) * ci.qty)}`)
    .join("\n");
  
  const message = `Halo ${store.value.name}! 🛒\n\nSaya ingin order:\n${itemsText}\n\nTotal: ${formatRp(cartTotal.value)}\n\nMohon info ongkir dan pembayaran. Terima kasih!`;
  
  window.open(`https://wa.me/${store.value.whatsapp}?text=${encodeURIComponent(message)}`, "_blank");
  checkoutDone.value = true;
  setTimeout(() => {
    checkoutDone.value = false;
  }, 4000);
};
</script>
