<template>
  <div class="min-h-screen bg-background text-foreground font-sans antialiased">
    <!-- Loading State -->
    <div v-if="isLoading" class="min-h-screen flex flex-col items-center justify-center bg-background p-6">
      <RefreshCw class="h-10 w-10 text-primary animate-spin" />
      <p class="text-sm font-semibold text-muted-foreground mt-3">Loading checkout form...</p>
    </div>

    <!-- Store Not Found -->
    <div v-else-if="!store" class="min-h-screen flex flex-col items-center justify-center bg-background p-6 text-center animate-fade-in">
      <Store class="h-16 w-16 text-muted-foreground mb-4" />
      <h1 class="text-2xl font-bold mb-2">Toko tidak ditemukan</h1>
      <router-link to="/">
        <button class="h-10 px-4 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm">
          Kembali
        </button>
      </router-link>
    </div>

    <!-- Cart Empty Fallback -->
    <div v-else-if="cartItems.length === 0 && !orderSuccess" class="min-h-screen flex flex-col items-center justify-center bg-background p-6 text-center animate-fade-in">
      <Package class="h-16 w-16 text-muted-foreground mb-4" />
      <h1 class="text-xl font-bold mb-2">Keranjang Kosong</h1>
      <p class="text-sm text-muted-foreground mb-6">Tambahkan produk terlebih dahulu sebelum checkout.</p>
      <button @click="backToStore" class="h-10 px-5 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm flex items-center gap-1.5 focus:outline-none">
        <ArrowLeft class="h-4 w-4" /> Kembali ke Toko
      </button>
    </div>

    <!-- Order Placed Success screen -->
    <div v-else-if="orderSuccess && createdOrder" class="min-h-screen bg-background flex items-center justify-center p-4">
      <div class="max-w-md w-full text-center space-y-5 animate-scale-in">
        <div class="mx-auto h-20 w-20 rounded-full bg-success/10 flex items-center justify-center border border-success/20">
          <CheckCircle2 class="h-10 w-10 text-success animate-bounce" />
        </div>
        <h1 class="text-2xl font-extrabold text-foreground">Pesanan Berhasil! 🎉</h1>
        <p class="text-muted-foreground text-sm leading-relaxed">
          Terima kasih telah berbelanja di <strong>{{ store.name }}</strong>. Detail pesanan telah disimpan ke sistem dan siap diproses.
        </p>
        <div class="bg-card border rounded-xl p-4 space-y-2 text-xs sm:text-sm text-left shadow-sm">
          <div class="flex justify-between border-b pb-1.5"><span class="text-muted-foreground">Order ID</span><span class="font-mono font-bold">{{ createdOrder.id }}</span></div>
          <div class="flex justify-between border-b pb-1.5"><span class="text-muted-foreground">Total Pembayaran</span><span class="font-bold text-primary">{{ formatRp(createdOrder.total) }}</span></div>
          <div class="flex justify-between border-b pb-1.5"><span class="text-muted-foreground">Pengiriman</span><span>{{ createdOrder.shipping_method }}</span></div>
          <div class="flex justify-between"><span class="text-muted-foreground">Estimasi Tiba</span><span>{{ createdOrder.estimated_delivery }}</span></div>
        </div>
        <div class="flex flex-col gap-2">
          <!-- Direct gateway link -->
          <a v-if="createdOrder.payment_url" :href="createdOrder.payment_url" target="_blank">
            <button class="w-full h-11 bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all rounded-xl shadow-sm flex items-center justify-center gap-2">
              <CreditCard class="h-4.5 w-4.5" /> Bayar Sekarang (Gateway API)
            </button>
          </a>
          <router-link :to="`/track?id=${createdOrder.id}`">
            <button class="w-full h-11 border hover:bg-muted text-foreground font-semibold text-sm transition-all rounded-xl shadow-sm flex items-center justify-center gap-2">
              <Package class="h-4.5 w-4.5" /> Lacak Pesanan
            </button>
          </router-link>
          <a :href="`https://wa.me/${store.whatsapp}?text=${encodeURIComponent(`Halo, saya baru saja melakukan pemesanan dengan Order ID ${createdOrder.id}. Mohon konfirmasinya.`)}`" target="_blank">
            <button class="w-full h-11 border hover:bg-muted text-foreground font-semibold text-sm transition-all rounded-xl shadow-sm flex items-center justify-center gap-2">
              <MessageCircle class="h-4.5 w-4.5 text-emerald-500" /> Hubungi Penjual
            </button>
          </a>
          <button @click="backToStore" class="w-full h-10 hover:bg-muted text-muted-foreground font-semibold text-xs transition-all rounded-xl">
            Kembali ke Toko
          </button>
        </div>
      </div>
    </div>

    <!-- Active Checkout Flow -->
    <div v-else class="flex flex-col justify-between min-h-screen">
      <!-- Header -->
      <header class="sticky top-0 z-40 bg-card/95 backdrop-blur-md border-b">
        <div class="max-w-3xl mx-auto px-4 h-14 flex items-center gap-3">
          <button @click="prevStep" class="p-2 -ml-2 rounded-lg hover:bg-muted text-muted-foreground focus:outline-none">
            <ArrowLeft class="h-4.5 w-4.5" />
          </button>
          <h1 class="font-bold text-sm flex-1 text-left">Checkout</h1>
          <span class="px-2.5 py-0.5 rounded-full bg-secondary text-secondary-foreground text-[10px] font-bold">{{ store.name }}</span>
        </div>
      </header>

      <!-- Stepper Progress Tracker -->
      <div class="max-w-3xl mx-auto px-4 py-4 w-full">
        <div class="flex items-center gap-1.5">
          <div v-for="(s, idx) in steps" :key="s.n" class="flex items-center flex-1 last:flex-none">
            <div :class="['flex items-center gap-2', step >= s.n ? 'text-primary' : 'text-muted-foreground']">
              <span 
                :class="[
                  'h-7 w-7 rounded-full text-xs font-bold flex items-center justify-center shrink-0 transition-colors',
                  step > s.n ? 'bg-primary text-primary-foreground' : step === s.n ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground border'
                ]"
              >
                {{ step > s.n ? "✓" : s.n }}
              </span>
              <span class="text-xs font-bold hidden sm:inline">{{ s.label }}</span>
            </div>
            <div v-if="idx < 3" :class="['flex-1 h-0.5 mx-2 rounded', step > s.n ? 'bg-primary' : 'bg-muted']" />
          </div>
        </div>
      </div>

      <!-- Checkout Container -->
      <div class="max-w-3xl mx-auto px-4 pb-32 w-full flex-1">
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-5">
          <!-- Stepper Form Details -->
          <div class="lg:col-span-3 space-y-4">
            
            <!-- STEP 1: Address -->
            <div v-if="step === 1" class="bg-card border rounded-2xl p-5 space-y-4 shadow-sm text-left animate-fade-in">
              <div class="flex items-center gap-2 border-b pb-3 mb-1">
                <MapPin class="h-4.5 w-4.5 text-primary" />
                <h2 class="font-bold text-sm sm:text-base">Alamat Pengiriman</h2>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">Nama Lengkap *</label>
                  <input type="text" placeholder="Nama penerima" v-model="form.name" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">No. HP / WhatsApp *</label>
                  <input type="text" placeholder="08xxxxxxxxxx" v-model="form.phone" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">Provinsi</label>
                  <input type="text" placeholder="DKI Jakarta" v-model="form.province" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">Kota / Kabupaten *</label>
                  <input type="text" placeholder="Jakarta Selatan" v-model="form.city" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">Kecamatan</label>
                  <input type="text" placeholder="Kebayoran Baru" v-model="form.district" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
                <div class="space-y-1.5">
                  <label class="text-[11px] font-bold text-muted-foreground uppercase">Kode Pos</label>
                  <input type="text" placeholder="12120" v-model="form.postalCode" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
                </div>
              </div>

              <div class="space-y-1.5">
                <label class="text-[11px] font-bold text-muted-foreground uppercase">Alamat Lengkap *</label>
                <textarea placeholder="Jl. Sudirman No. 123, RT 01/RW 02, Blok A..." v-model="form.address" rows="3" class="w-full bg-card border rounded-lg p-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20"></textarea>
              </div>

              <div class="space-y-1.5">
                <label class="text-[11px] font-bold text-muted-foreground uppercase">Catatan untuk Kurir</label>
                <input type="text" placeholder="Lantai 3, pintu warna biru, dll." v-model="form.notes" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
              </div>

              <button 
                :disabled="!isAddressValid" 
                @click="goToStep2" 
                class="w-full h-11 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed outline-none"
              >
                Lanjut ke Pengiriman <ChevronRight class="h-4 w-4" />
              </button>
            </div>

            <!-- STEP 2: Shipping -->
            <div v-if="step === 2" class="bg-card border rounded-2xl p-5 space-y-4 shadow-sm text-left animate-fade-in">
              <div class="flex items-center gap-2 border-b pb-3 mb-1">
                <Truck class="h-4.5 w-4.5 text-primary" />
                <h2 class="font-bold text-sm sm:text-base">Pilih Pengiriman</h2>
              </div>

              <div class="flex gap-2 flex-wrap pb-1">
                <button
                  @click="shippingFilter = 'all'"
                  :class="[
                    'px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all focus:outline-none',
                    shippingFilter === 'all' ? 'bg-primary border-primary text-primary-foreground shadow-sm' : 'bg-muted border-transparent text-muted-foreground hover:bg-muted/80'
                  ]"
                >
                  Semua
                </button>
                <button
                  v-for="cat in shippingCategories"
                  :key="cat"
                  @click="shippingFilter = cat"
                  :class="[
                    'px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all focus:outline-none',
                    shippingFilter === cat ? 'bg-primary border-primary text-primary-foreground shadow-sm' : 'bg-muted border-transparent text-muted-foreground hover:bg-muted/80'
                  ]"
                >
                  {{ cat }}
                </button>
              </div>

              <div v-if="isLoadingRates" class="text-center py-10">
                <RefreshCw class="h-8 w-8 text-primary animate-spin mx-auto" />
                <p class="text-xs text-muted-foreground mt-2">Menghitung tarif kurir (Logistics API)...</p>
              </div>
              <div v-else-if="filteredShippingOptions.length === 0" class="text-center py-10 text-muted-foreground">
                <p class="text-xs font-semibold">Kurir tidak tersedia untuk kota tujuan ini.</p>
              </div>
              <div v-else class="space-y-2">
                <button
                  v-for="opt in filteredShippingOptions"
                  :key="opt.id"
                  @click="selectedShipping = opt.id"
                  :class="[
                    'w-full flex items-center gap-3.5 p-3.5 rounded-xl border text-left transition-all outline-none',
                    selectedShipping === opt.id
                      ? 'border-primary bg-accent/40 ring-1 ring-primary/20 shadow-sm'
                      : 'border-border bg-card hover:border-primary/20 hover:bg-muted/20'
                  ]"
                >
                  <div 
                    :class="[
                      'p-2.5 rounded-lg shrink-0',
                      opt.type === 'Instant' ? 'bg-amber-500/10 text-amber-500' :
                      opt.type === 'Same Day' ? 'bg-cyan-500/10 text-cyan-500' :
                      opt.type === 'Ekonomi' ? 'bg-slate-500/10 text-slate-500' :
                      'bg-primary/10 text-primary'
                    ]"
                  >
                    <component :is="opt.icon" class="h-4.5 w-4.5" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2">
                      <span class="text-xs sm:text-sm font-bold text-foreground">{{ opt.name }}</span>
                      <span v-if="opt.popular" class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 text-[8px] font-bold uppercase leading-none">Populer</span>
                    </div>
                    <p class="text-xs text-muted-foreground mt-0.5">Estimasi: {{ opt.eta }}</p>
                  </div>
                  <div class="text-right shrink-0">
                    <p class="text-xs sm:text-sm font-extrabold text-foreground">{{ formatRp(opt.price) }}</p>
                    <span class="px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground text-[8px] font-bold uppercase tracking-wider mt-1 inline-block">{{ opt.type }}</span>
                  </div>
                  <div 
                    :class="[
                      'h-5 w-5 rounded-full border-2 shrink-0 flex items-center justify-center transition-all',
                      selectedShipping === opt.id ? 'border-primary bg-primary' : 'border-muted-foreground/30'
                    ]"
                  >
                    <span v-if="selectedShipping === opt.id" class="h-2 w-2 rounded-full bg-primary-foreground"></span>
                  </div>
                </button>
              </div>

              <button 
                :disabled="!selectedShipping" 
                @click="step = 3" 
                class="w-full h-11 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed outline-none"
              >
                Lanjut ke Pembayaran <ChevronRight class="h-4 w-4" />
              </button>
            </div>

            <!-- STEP 3: Payment Method -->
            <div v-if="step === 3" class="bg-card border rounded-2xl p-5 space-y-4 shadow-sm text-left animate-fade-in">
              <div class="flex items-center gap-2 border-b pb-3 mb-1">
                <CreditCard class="h-4.5 w-4.5 text-primary" />
                <h2 class="font-bold text-sm sm:text-base">Metode Pembayaran</h2>
              </div>

              <div class="space-y-2">
                <button
                  v-for="pm in paymentMethods"
                  :key="pm.id"
                  @click="selectedPayment = pm.id"
                  :class="[
                    'w-full flex items-center gap-3.5 p-4 rounded-xl border text-left transition-all outline-none',
                    selectedPayment === pm.id
                      ? 'border-primary bg-accent/40 ring-1 ring-primary/20 shadow-sm'
                      : 'border-border bg-card hover:border-primary/20 hover:bg-muted/20'
                  ]"
                >
                  <div class="p-2.5 rounded-lg bg-muted shrink-0 text-foreground">
                    <component :is="pm.icon" class="h-5 w-5" />
                  </div>
                  <div class="flex-1">
                    <p class="text-xs sm:text-sm font-bold text-foreground leading-none">{{ pm.name }}</p>
                    <p class="text-xs text-muted-foreground mt-1">{{ pm.desc }}</p>
                  </div>
                  <div 
                    :class="[
                      'h-5 w-5 rounded-full border-2 shrink-0 flex items-center justify-center transition-all',
                      selectedPayment === pm.id ? 'border-primary bg-primary' : 'border-muted-foreground/30'
                    ]"
                  >
                    <span v-if="selectedPayment === pm.id" class="h-2 w-2 rounded-full bg-primary-foreground"></span>
                  </div>
                </button>
              </div>

              <div class="flex items-start gap-2 p-3 rounded-lg bg-accent/30 border text-xs text-muted-foreground">
                <Shield class="h-4.5 w-4.5 text-primary mt-0.5 shrink-0" />
                <span>Transaksi Anda dilindungi secara penuh. Data pembayaran dienkripsi secara aman.</span>
              </div>

              <button 
                :disabled="!selectedPayment" 
                @click="step = 4" 
                class="w-full h-11 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed outline-none"
              >
                Tinjau Pesanan <ChevronRight class="h-4 w-4" />
              </button>
            </div>

            <!-- STEP 4: Summary Review -->
            <div v-if="step === 4" class="space-y-4 animate-fade-in text-left">
              <!-- Address -->
              <div class="bg-card border rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-3 border-b pb-2">
                  <div class="flex items-center gap-2 text-foreground font-bold">
                    <MapPin class="h-4.5 w-4.5 text-primary" />
                    <span class="text-sm">Alamat Pengiriman</span>
                  </div>
                  <button @click="step = 1" class="text-xs font-bold text-primary hover:underline focus:outline-none">Ubah</button>
                </div>
                <div class="text-xs sm:text-sm space-y-1 text-foreground">
                  <p class="font-bold">{{ form.name }} · {{ form.phone }}</p>
                  <p class="text-muted-foreground leading-snug">{{ form.address }}</p>
                  <p class="text-muted-foreground leading-snug">
                    {{ [form.district, form.city, form.province, form.postalCode].filter(Boolean).join(", ") }}
                  </p>
                  <p v-if="form.notes" class="text-xs text-muted-foreground italic pt-1 flex items-center gap-1">
                    📝 {{ form.notes }}
                  </p>
                </div>
              </div>

              <!-- Shipping -->
              <div class="bg-card border rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-3 border-b pb-2">
                  <div class="flex items-center gap-2 text-foreground font-bold">
                    <Truck class="h-4.5 w-4.5 text-primary" />
                    <span class="text-sm">Pengiriman</span>
                  </div>
                  <button @click="step = 2" class="text-xs font-bold text-primary hover:underline focus:outline-none">Ubah</button>
                </div>
                <div class="flex justify-between items-center text-xs sm:text-sm text-foreground" v-if="shippingObj">
                  <div>
                    <p class="font-bold">{{ shippingObj.name }}</p>
                    <p class="text-xs text-muted-foreground mt-0.5">Estimasi: {{ shippingObj.eta }}</p>
                  </div>
                  <span class="font-bold">{{ formatRp(shippingObj.price) }}</span>
                </div>
              </div>

              <!-- Payment -->
              <div class="bg-card border rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-3 border-b pb-2">
                  <div class="flex items-center gap-2 text-foreground font-bold">
                    <CreditCard class="h-4.5 w-4.5 text-primary" />
                    <span class="text-sm">Pembayaran</span>
                  </div>
                  <button @click="step = 3" class="text-xs font-bold text-primary hover:underline focus:outline-none">Ubah</button>
                </div>
                <p class="text-xs sm:text-sm font-bold text-foreground" v-if="paymentObj">
                  {{ paymentObj.name }}
                </p>
              </div>

              <!-- Cart preview list -->
              <div class="bg-card border rounded-2xl p-4 shadow-sm space-y-3">
                <h3 class="font-bold text-sm text-foreground">Produk ({{ itemCount }} item)</h3>
                <div class="divide-y">
                  <div v-for="item in cartItems" :key="item.id" class="flex items-center gap-3 py-2.5">
                    <img :src="item.product.img" :alt="item.product.name" class="h-11 w-11 rounded-lg object-cover shrink-0 bg-muted border" />
                    <div class="flex-1 min-w-0">
                      <p class="text-xs sm:text-sm font-bold text-foreground truncate leading-snug">{{ item.product.name }}</p>
                      <p class="text-[10px] sm:text-xs text-muted-foreground mt-0.5">{{ item.qty }}x {{ formatRp(getPrice(item.product)) }}</p>
                    </div>
                    <span class="text-xs sm:text-sm font-bold text-foreground shrink-0">{{ formatRp(getPrice(item.product) * item.qty) }}</span>
                  </div>
                </div>
              </div>

              <button 
                @click="placeOrder" 
                class="w-full h-12 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-2 focus:outline-none"
              >
                <CheckCircle2 class="h-4.5 w-4.5" /> Bayar {{ formatRp(total) }}
              </button>
            </div>
          </div>

          <!-- Order Summary Sidebar panel -->
          <div class="lg:col-span-2 text-left">
            <div class="sticky top-20 space-y-3">
              <div class="bg-card border rounded-2xl p-4 shadow-sm space-y-3">
                <h3 class="font-bold text-sm text-foreground">Ringkasan Pesanan</h3>
                
                <div class="divide-y max-h-[220px] overflow-y-auto pr-1 scrollbar-thin">
                  <div v-for="item in cartItems" :key="item.id" class="flex items-center gap-2.5 py-2">
                    <img :src="item.product.img" :alt="item.product.name" class="h-9 w-9 rounded-lg object-cover shrink-0 bg-muted border" />
                    <div class="flex-1 min-w-0">
                      <p class="text-[11px] sm:text-xs font-semibold text-foreground truncate leading-snug">{{ item.product.name }}</p>
                      <p class="text-[10px] text-muted-foreground mt-0.5">{{ item.qty }}x</p>
                    </div>
                    <span class="text-[11px] sm:text-xs font-bold text-foreground shrink-0">{{ formatRp(getPrice(item.product) * item.qty) }}</span>
                  </div>
                </div>

                <div class="space-y-2 pt-3 border-t text-xs sm:text-sm">
                  <div class="flex justify-between text-muted-foreground">
                    <span>Subtotal ({{ itemCount }} item)</span>
                    <span class="text-foreground font-semibold">{{ formatRp(subtotal) }}</span>
                  </div>
                  <div class="flex justify-between text-muted-foreground">
                    <span>Ongkos Kirim</span>
                    <span class="text-foreground font-semibold">{{ shippingObj ? formatRp(shippingCost) : "—" }}</span>
                  </div>
                  <div class="flex justify-between pt-2 border-t font-bold text-foreground text-sm sm:text-base">
                    <span>Total Tagihan</span>
                    <span class="text-primary">{{ formatRp(total) }}</span>
                  </div>
                </div>
              </div>

              <!-- Estimated Delivery summary box -->
              <div class="flex items-start gap-2.5 p-4 rounded-2xl bg-accent/30 border border-primary/10" v-if="shippingObj">
                <Truck class="h-5 w-5 text-primary shrink-0 mt-0.5" />
                <div class="text-xs">
                  <p class="font-bold text-foreground">{{ shippingObj.name }}</p>
                  <p class="text-muted-foreground mt-0.5">Estimasi tiba: {{ shippingObj.eta }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import {
  ArrowLeft,
  MapPin,
  Truck,
  Clock,
  Zap,
  Package,
  CreditCard,
  Banknote,
  QrCode,
  Smartphone,
  Shield,
  CheckCircle2,
  ChevronRight,
  MessageCircle,
  RefreshCw
} from "lucide-vue-next";

// Setup Types
interface CartItem {
  id: number;
  product: {
    id: number;
    name: string;
    price: number;
    stock: number;
    img: string;
  };
  qty: number;
}

interface ShippingOption {
  id: string;
  name: string;
  courier: string;
  type: string;
  price: number;
  eta: string;
  icon: any;
  popular?: boolean;
}

const steps = [
  { n: 1, label: "Alamat" },
  { n: 2, label: "Pengiriman" },
  { n: 3, label: "Pembayaran" },
  { n: 4, label: "Konfirmasi" },
];

const shippingOptions = ref<ShippingOption[]>([]);
const isLoadingRates = ref(false);

const fetchShippingRates = async () => {
  if (!form.value.city) return;
  isLoadingRates.value = true;
  try {
    const payload = {
      city: form.value.city,
      items: cartItems.value.map((i) => ({
        product_id: i.id,
        qty: i.qty,
        price: getPrice(i.product)
      }))
    };
    const res = await axios.post("/api/shipping/rates", payload);
    shippingOptions.value = res.data.map((opt: any) => {
      let iconComponent = Truck;
      if (opt.type === "Instant") iconComponent = Zap;
      else if (opt.type === "Same Day") iconComponent = Clock;
      else if (opt.type === "Ekonomi") iconComponent = Package;
      return {
        ...opt,
        icon: iconComponent
      };
    });
    if (shippingOptions.value.length > 0) {
      selectedShipping.value = shippingOptions.value[0].id;
    } else {
      selectedShipping.value = null;
    }
  } catch (error) {
    console.error("Error fetching shipping rates:", error);
    shippingOptions.value = [];
  } finally {
    isLoadingRates.value = false;
  }
};

const goToStep2 = async () => {
  step.value = 2;
  await fetchShippingRates();
};

const shippingCategories = ["Instant", "Same Day", "Reguler", "Ekonomi"];

const paymentMethods = [
  { id: "qris", name: "QRIS", icon: QrCode, desc: "GoPay, OVO, DANA, ShopeePay, dll" },
  { id: "va-bca", name: "Transfer Bank (VA)", icon: CreditCard, desc: "BCA, BNI, BRI, Mandiri, Permata" },
  { id: "ewallet", name: "E-Wallet", icon: Smartphone, desc: "GoPay, OVO, DANA" },
  { id: "cod", name: "COD (Bayar di Tempat)", icon: Banknote, desc: "Bayar saat barang sampai" },
];

const route = useRoute();
const router = useRouter();
const storeName = route.params.storeName as string;

const store = ref<any>(null);
const cartItems = ref<CartItem[]>([]);
const isLoading = ref(true);
const orderSuccess = ref(false);
const createdOrder = ref<any>(null);

// Forms state
const step = ref(1);
const form = ref({
  name: "",
  phone: "",
  province: "",
  city: "",
  district: "",
  postalCode: "",
  address: "",
  notes: ""
});
const selectedShipping = ref<string | null>(null);
const selectedPayment = ref<string | null>(null);
const shippingFilter = ref("all");

const getPrice = (p: any) => {
  if (!store.value) return p.price;
  return Math.round(p.price * (1 + (store.value.markup ?? 0) / 100));
};

const formatRp = (n: number) => `Rp ${n.toLocaleString("id-ID")}`;

const backToStore = () => {
  router.push(`/store/${storeName}`);
};

const loadCheckoutContext = async () => {
  try {
    const storeRes = await axios.get(`/api/stores/${storeName}`);
    store.value = storeRes.data;

    const savedCart = sessionStorage.getItem(`cart_${storeName}`);
    if (savedCart) {
      cartItems.value = JSON.parse(savedCart);
    }
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadCheckoutContext();
});

// Calculations
const subtotal = computed(() => {
  return cartItems.value.reduce((s, item) => s + getPrice(item.product) * item.qty, 0);
});

const shippingObj = computed(() => {
  return shippingOptions.value.find((s) => s.id === selectedShipping.value) || null;
});

const paymentObj = computed(() => {
  return paymentMethods.find((pm) => pm.id === selectedPayment.value) || null;
});

const shippingCost = computed(() => {
  return shippingObj.value ? shippingObj.value.price : 0;
});

const total = computed(() => {
  return subtotal.value + shippingCost.value;
});

const itemCount = computed(() => {
  return cartItems.value.reduce((s, i) => s + i.qty, 0);
});

const isAddressValid = computed(() => {
  return form.value.name.trim() !== "" &&
    form.value.phone.trim() !== "" &&
    form.value.city.trim() !== "" &&
    form.value.address.trim() !== "";
});

const filteredShippingOptions = computed(() => {
  if (shippingFilter.value === "all") return shippingOptions.value;
  return shippingOptions.value.filter((s) => s.type === shippingFilter.value);
});

const prevStep = () => {
  if (step.value > 1) {
    step.value--;
  } else {
    backToStore();
  }
};

// Place Order API call
const placeOrder = async () => {
  if (!store.value || !shippingObj.value || !paymentObj.value) return;

  const payload = {
    store_slug: store.value.slug,
    customer_name: form.value.name,
    customer_phone: form.value.phone,
    address: form.value.address,
    city: [form.value.district, form.value.city, form.value.province, form.value.postalCode].filter(Boolean).join(", "),
    shipping_method: shippingObj.value.name,
    shipping_courier: shippingObj.value.courier,
    shipping_cost: shippingObj.value.price,
    payment_method: paymentObj.value.name,
    items: cartItems.value.map((i) => ({
      product_id: i.id,
      qty: i.qty,
      price: getPrice(i.product)
    }))
  };

  try {
    const res = await axios.post("/api/orders", payload);
    createdOrder.value = res.data;

    // Success flow
    sessionStorage.removeItem(`cart_${storeName}`);
    orderSuccess.value = true;
  } catch (error: any) {
    console.error(error);
    alert(error.response?.data?.detail || "Gagal membuat pesanan. Silakan coba lagi.");
  }
};
</script>
