<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Webstore & POS</h1>
        <p class="text-muted-foreground text-sm mt-1">Unified commerce across online and offline channels.</p>
      </div>
      <div class="flex items-center gap-3 bg-card border rounded-xl px-4 py-2.5 shadow-sm">
        <Smartphone class="h-4 w-4 text-primary" />
        <span class="text-sm font-medium">AI Store Manager</span>
        <button 
          @click="aiManager = !aiManager" 
          :class="[
            'relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none',
            aiManager ? 'bg-primary' : 'bg-muted'
          ]"
        >
          <span 
            :class="[
              'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-background shadow ring-0 transition duration-200 ease-in-out',
              aiManager ? 'translate-x-5' : 'translate-x-0'
            ]"
          />
        </button>
        <span 
          :class="[
            'text-[10px] font-semibold px-2 py-0.5 rounded-full',
            aiManager ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'
          ]"
        >
          {{ aiManager ? "● Active" : "Off" }}
        </span>
      </div>
    </div>

    <!-- Channel Stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="ch in channels" :key="ch.name" class="bg-card border rounded-xl p-4 overflow-hidden hover:shadow-md transition-all">
        <div class="flex items-center justify-between mb-3">
          <span class="text-lg">{{ ch.icon }}</span>
          <span class="h-2 w-2 rounded-full bg-success" />
        </div>
        <p class="text-xs text-muted-foreground">{{ ch.name }}</p>
        <p class="text-xl font-bold mt-0.5">{{ ch.revenue }}</p>
        <div class="flex items-center gap-1 mt-1 text-success">
          <ArrowUpRight class="h-3 w-3" />
          <span class="text-xs font-semibold">{{ ch.orders }} orders</span>
        </div>
      </div>
    </div>

    <!-- Main Tabs -->
    <div class="space-y-4">
      <div class="flex border-b border-border overflow-x-auto gap-2 py-1">
        <button
          v-for="tab in tabsList"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'flex items-center gap-2 px-4 py-2.5 text-sm font-semibold rounded-lg whitespace-nowrap transition-all border',
            activeTab === tab.value
              ? 'bg-primary text-primary-foreground border-primary shadow-sm'
              : 'bg-card border-transparent text-muted-foreground hover:bg-muted/60 hover:text-foreground'
          ]"
        >
          <component :is="tab.icon" class="h-4 w-4" />
          {{ tab.label }}
        </button>
      </div>

      <!-- ─── MY STORE TAB ─────────────────── -->
      <div v-if="activeTab === 'mystore'" class="space-y-4">
        <!-- Share Card -->
        <div class="bg-card border border-primary/20 bg-gradient-to-br from-accent/30 to-background rounded-xl p-6 shadow-sm overflow-hidden">
          <div class="flex flex-col md:flex-row md:items-center gap-5">
            <div class="h-16 w-16 rounded-2xl bg-primary flex items-center justify-center shrink-0 shadow-md">
              <Store class="h-8 w-8 text-primary-foreground" />
            </div>
            <div class="flex-1 space-y-1">
              <h2 class="text-lg font-bold text-foreground">{{ ownerStore.name }}</h2>
              <p class="text-sm text-muted-foreground">{{ ownerStore.tagline }}</p>
              <div class="flex flex-col sm:flex-row gap-2 mt-3">
                <div class="flex-1 flex items-center gap-2 bg-card border rounded-lg px-3 py-2">
                  <LinkIcon class="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                  <span class="text-xs sm:text-sm font-mono truncate text-foreground">{{ storeUrl(ownerStore.slug) }}</span>
                </div>
                <div class="flex gap-2 shrink-0">
                  <button @click="copyLink(ownerStore.slug)" class="h-10 px-4 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs transition-all flex items-center gap-1.5 shadow-sm">
                    <component :is="copiedLink === ownerStore.slug ? Check : Copy" class="h-3.5 w-3.5" />
                    {{ copiedLink === ownerStore.slug ? "Tersalin!" : "Copy Link" }}
                  </button>
                  <a :href="storeUrl(ownerStore.slug)" target="_blank" class="h-10 px-4 rounded-lg bg-card border hover:bg-muted text-foreground font-semibold text-xs transition-all flex items-center gap-1.5 shadow-sm">
                    <ExternalLink class="h-3.5 w-3.5" />
                    Lihat Toko
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters & Sort -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div class="flex items-center gap-3">
            <h3 class="font-bold text-sm">Produk di Webstore</h3>
            <span class="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-xs font-semibold">
              {{ activeProductsCount }} aktif
            </span>
          </div>
          <!-- Sort Option Selection -->
          <div class="relative shrink-0">
            <select v-model="storeSort" class="h-8 pl-8 pr-4 bg-card border rounded-lg text-xs font-semibold focus:outline-none cursor-pointer">
              <option v-for="(lbl, val) in sortLabels" :key="val" :value="val">{{ lbl }}</option>
            </select>
            <ArrowUpDown class="h-3.5 w-3.5 text-muted-foreground absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        <!-- Category Chips -->
        <div class="flex items-center gap-2 flex-wrap">
          <button 
            @click="selectedCategory = 'Semua'"
            :class="[
              'px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all',
              selectedCategory === 'Semua' 
                ? 'bg-primary text-primary-foreground border-primary shadow-sm'
                : 'bg-card text-muted-foreground border-border hover:bg-accent/40 hover:text-foreground'
            ]"
          >
            📦 Semua
          </button>
          <button 
            v-for="cat in categoryList"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            :class="[
              'px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all',
              selectedCategory === cat.id 
                ? 'bg-primary text-primary-foreground border-primary shadow-sm'
                : 'bg-card text-muted-foreground border-border hover:bg-accent/40 hover:text-foreground'
            ]"
          >
            {{ cat.icon }} {{ cat.name }}
          </button>
        </div>

        <!-- Webstore Product Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-3">
          <div 
            v-for="p in filteredWebstoreProducts" 
            :key="p.id" 
            class="bg-card border rounded-xl overflow-hidden group hover:shadow-md transition-shadow flex flex-col justify-between"
          >
            <div class="aspect-square overflow-hidden bg-muted relative">
              <img :src="p.img" :alt="p.name" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
            </div>
            <div class="p-3 space-y-1.5">
              <p class="text-[10px] text-muted-foreground">{{ categoryLabel(p.category) }}</p>
              <h4 class="text-xs font-bold text-foreground truncate">{{ p.name }}</h4>
              <p class="text-sm font-bold text-primary">{{ formatRp(p.price) }}</p>
              <div class="flex items-center gap-1 text-[10px] text-muted-foreground">
                <Star class="h-3 w-3 fill-warning text-warning" />
                <span>{{ p.rating }} · {{ p.sold }} terjual</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── RESELLERS TAB ────────────────── -->
      <div v-if="activeTab === 'resellers'" class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="font-bold text-base text-foreground">Reseller Partners</h3>
            <p class="text-xs text-muted-foreground mt-0.5">Reseller menjual produk Anda dengan nama toko mereka sendiri dan markup harga.</p>
          </div>
          <button @click="addReseller" class="h-8 px-3 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs transition-all flex items-center gap-1">
            <Plus class="h-3.5 w-3.5" /> Tambah Reseller
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <div v-for="rs in resellerStores" :key="rs.slug" class="bg-card border rounded-xl p-5 space-y-4 hover:shadow-md transition-shadow">
            <div class="flex items-start gap-3">
              <div class="h-11 w-11 rounded-xl bg-accent flex items-center justify-center shrink-0">
                <Store class="h-5 w-5 text-accent-foreground" />
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-bold text-sm text-foreground">{{ rs.name }}</h4>
                <p class="text-xs text-muted-foreground">by {{ rs.owner }}</p>
              </div>
              <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] font-semibold shrink-0">Active</span>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="rounded-lg bg-muted/50 p-2.5 text-center">
                <Percent class="h-4 w-4 mx-auto text-muted-foreground mb-1" />
                <p class="text-lg font-bold text-foreground">{{ rs.markup }}%</p>
                <p class="text-[10px] text-muted-foreground">Markup</p>
              </div>
              <div class="rounded-lg bg-muted/50 p-2.5 text-center">
                <ShoppingBag class="h-4 w-4 mx-auto text-muted-foreground mb-1" />
                <p class="text-lg font-bold text-foreground">{{ activeProductsCount }}</p>
                <p class="text-[10px] text-muted-foreground">Produk</p>
              </div>
            </div>

            <div class="flex items-center gap-2 bg-muted/40 rounded-lg px-3 py-2 border">
              <LinkIcon class="h-3 w-3 text-muted-foreground shrink-0" />
              <span class="text-xs font-mono truncate flex-1 text-foreground">/store/{{ rs.slug }}</span>
              <button @click="copyLink(rs.slug)" class="p-1 rounded hover:bg-muted transition-colors">
                <component :is="copiedLink === rs.slug ? Check : Copy" class="h-3.5 w-3.5" :class="copiedLink === rs.slug ? 'text-success' : 'text-muted-foreground'" />
              </button>
              <a :href="storeUrl(rs.slug)" target="_blank">
                <ExternalLink class="h-3.5 w-3.5 text-muted-foreground hover:text-foreground" />
              </a>
            </div>

            <p class="text-xs text-muted-foreground italic leading-snug">"{{ rs.tagline }}"</p>
          </div>
        </div>
      </div>

      <!-- ─── POS TAB ──────────────────────── -->
      <div v-if="activeTab === 'pos'" class="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <!-- Products selection pane -->
        <div class="lg:col-span-3 space-y-3">
          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Scan barcode atau cari produk / SKU..."
                v-model="posSearch"
                class="pl-9 h-11 w-full bg-card border rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/30"
              />
            </div>
            <div class="relative shrink-0">
              <select v-model="posSort" class="h-8 pl-8 pr-4 bg-card border rounded-lg text-xs font-semibold focus:outline-none cursor-pointer">
                <option v-for="(lbl, val) in sortLabels" :key="val" :value="val">{{ lbl }}</option>
              </select>
              <ArrowUpDown class="h-3.5 w-3.5 text-muted-foreground absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>
          
          <div class="flex items-center gap-2 flex-wrap">
            <button 
              @click="posCategory = 'Semua'"
              :class="[
                'px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all',
                posCategory === 'Semua' 
                  ? 'bg-primary text-primary-foreground border-primary shadow-sm'
                  : 'bg-card text-muted-foreground border-border hover:bg-accent/40 hover:text-foreground'
              ]"
            >
              📦 Semua
            </button>
            <button 
              v-for="cat in categoryList"
              :key="cat.id"
              @click="posCategory = cat.id"
              :class="[
                'px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all',
                posCategory === cat.id 
                  ? 'bg-primary text-primary-foreground border-primary shadow-sm'
                  : 'bg-card text-muted-foreground border-border hover:bg-accent/40 hover:text-foreground'
              ]"
            >
              {{ cat.icon }} {{ cat.name }}
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            <button
              v-for="p in posFilteredProducts"
              :key="p.id"
              @click="addToCart(p.id)"
              class="flex items-center gap-3 p-3 rounded-xl border bg-card hover:bg-accent/40 hover:border-primary/30 transition-all text-left active:scale-[0.98] outline-none"
            >
              <img :src="p.img" :alt="p.name" class="h-12 w-12 rounded-lg object-cover shrink-0 bg-muted" />
              <div class="min-w-0 flex-1">
                <p class="text-sm font-bold text-foreground truncate">{{ p.name }}</p>
                <p class="text-[10px] text-muted-foreground font-mono leading-none">{{ p.sku }}</p>
                <p class="text-xs font-bold text-primary mt-1">{{ formatRp(p.price) }}</p>
              </div>
              <span class="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-[10px] font-semibold shrink-0">
                Stok: {{ p.stock }}
              </span>
            </button>
          </div>
        </div>

        <!-- Cashier Cart sidebar -->
        <div class="lg:col-span-2 bg-card border rounded-xl flex flex-col justify-between shadow-sm overflow-hidden h-fit">
          <div class="p-4 border-b">
            <h3 class="font-bold text-base text-foreground flex items-center gap-2">
              <ShoppingCart class="h-4 w-4 text-primary" />
              POS Keranjang
              <span class="ml-auto px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-xs font-semibold">
                {{ cartCount }} item
              </span>
            </h3>
          </div>

          <!-- Cart list -->
          <div class="divide-y overflow-y-auto max-h-[300px] min-h-[160px]">
            <div v-if="cart.length === 0" class="p-8 text-center text-sm text-muted-foreground">
              Keranjang kosong. Tambahkan produk di sebelah kiri.
            </div>
            <div v-for="item in cart" :key="item.id" class="flex items-center gap-3 p-3 transition-colors hover:bg-muted/10">
              <img :src="item.product.img" :alt="item.product.name" class="h-10 w-10 rounded-lg object-cover shrink-0 bg-muted" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-foreground truncate leading-snug">{{ item.product.name }}</p>
                <p class="text-xs text-muted-foreground mt-0.5">{{ formatRp(item.product.price) }}</p>
              </div>
              <div class="flex items-center gap-1">
                <button @click="updateCartQty(item.id, -1)" class="h-7 w-7 rounded-md bg-muted hover:bg-muted/80 flex items-center justify-center font-bold text-sm focus:outline-none">-</button>
                <span class="text-sm font-semibold w-7 text-center">{{ item.qty }}</span>
                <button @click="updateCartQty(item.id, 1)" class="h-7 w-7 rounded-md bg-muted hover:bg-muted/80 flex items-center justify-center font-bold text-sm focus:outline-none">+</button>
              </div>
              <button @click="removeCartItem(item.id)" class="p-1.5 rounded-md hover:bg-destructive/10 text-destructive focus:outline-none transition-colors">
                <Trash2 class="h-4 w-4" />
              </button>
            </div>
          </div>

          <!-- Calculations -->
          <div class="border-t p-4 space-y-3 bg-muted/20">
            <div class="flex justify-between text-sm">
              <span class="text-muted-foreground">Subtotal</span>
              <span class="font-semibold text-foreground">{{ formatRp(cartSubtotal) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-muted-foreground">Pajak (11%)</span>
              <span class="font-semibold text-foreground">{{ formatRp(cartTax) }}</span>
            </div>
            <div class="flex justify-between text-base pt-2 border-t font-bold text-foreground">
              <span>Total</span>
              <span class="text-primary text-lg">{{ formatRp(cartTotal) }}</span>
            </div>

            <!-- Payment Type -->
            <div class="grid grid-cols-3 gap-2 pt-2">
              <button 
                v-for="pm in posPaymentMethods" 
                :key="pm.id"
                @click="selectedPaymentMethod = pm.id"
                :class="[
                  'flex flex-col items-center justify-center py-2 px-1 rounded-xl border text-center transition-all duration-200 gap-1.5 outline-none',
                  selectedPaymentMethod === pm.id 
                    ? 'border-primary bg-primary/5 text-primary ring-1 ring-primary/20' 
                    : 'border-border bg-card text-muted-foreground hover:bg-muted/50 hover:text-foreground'
                ]"
              >
                <component :is="pm.icon" class="h-4 w-4" />
                <span class="text-[9px] font-bold uppercase tracking-wider">{{ pm.label }}</span>
              </button>
            </div>

            <button 
              @click="openCheckoutModal"
              :disabled="cart.length === 0" 
              class="w-full h-11 rounded-xl bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed outline-none mt-2"
            >
              <ShoppingCart class="h-4 w-4" /> Proses Pembayaran
            </button>
          </div>
        </div>
      </div>

      <!-- ─── INVENTORY TAB ────────────────── -->
      <div v-if="activeTab === 'inventory'" class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2 text-sm text-muted-foreground">
            <BarChart3 class="h-4 w-4" />
            <span class="font-semibold">{{ products.length }} total produk · {{ activeProductsCount }} tersinkron</span>
          </div>
          <button @click="syncAllProducts" class="h-8 px-3 rounded-lg bg-card border hover:bg-muted text-foreground font-semibold text-xs transition-all flex items-center gap-1">
            <RefreshCw class="h-3.5 w-3.5" /> Sync Semua
          </button>
        </div>

        <div class="bg-card border rounded-xl overflow-hidden shadow-sm">
          <div class="overflow-x-auto">
            <table class="w-full text-sm text-left">
              <thead>
                <tr class="border-b bg-muted/40 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  <th class="py-3.5 px-4">Produk</th>
                  <th class="py-3.5 px-4">SKU</th>
                  <th class="py-3.5 px-4">Kategori</th>
                  <th class="py-3.5 px-4 text-right">Harga</th>
                  <th class="py-3.5 px-4 text-right">Stok POS</th>
                  <th class="py-3.5 px-4 text-right">Stok Online</th>
                  <th class="py-3.5 px-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-border">
                <tr v-for="p in products" :key="p.sku" class="hover:bg-muted/10 transition-colors">
                  <td class="py-3 px-4">
                    <div class="flex items-center gap-3">
                      <img :src="p.img" :alt="p.name" class="h-9 w-9 rounded-lg object-cover bg-muted shrink-0" />
                      <span class="font-semibold text-foreground text-xs sm:text-sm">{{ p.name }}</span>
                    </div>
                  </td>
                  <td class="py-3 px-4 font-mono text-xs text-muted-foreground">{{ p.sku }}</td>
                  <td class="py-3 px-4">
                    <span class="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-[10px] font-semibold">
                      {{ categoryLabel(p.category) }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-right font-bold text-foreground">{{ formatRp(p.price) }}</td>
                  <td class="py-3 px-4 text-right text-foreground">{{ p.stock }}</td>
                  <td class="py-3 px-4 text-right text-foreground">{{ p.online }}</td>
                  <td class="py-3 px-4 text-center">
                    <span 
                      :class="[
                        'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold leading-none',
                        p.status === 'synced' ? 'bg-primary/10 text-primary' :
                        p.status === 'syncing' ? 'bg-amber-500/10 text-amber-500' : 'bg-destructive/10 text-destructive'
                      ]"
                    >
                      {{ p.status === 'synced' ? '✓ Synced' : p.status === 'syncing' ? '⟳ Syncing' : '✕ Out' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ─── SETTINGS TAB ──────────────────── -->
      <div v-if="activeTab === 'settings'" class="space-y-6 animate-fade-in">
        <!-- Category Manager -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-base text-foreground flex items-center gap-2">
                <FolderPlus class="h-4.5 w-4.5 text-muted-foreground" />
                Manajemen Kategori
              </h3>
              <p class="text-xs text-muted-foreground mt-0.5">Kelola kategori produk untuk webstore, reseller, dan POS.</p>
            </div>
            <button @click="openCategoryForm(null)" class="h-8 px-3 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs transition-all flex items-center gap-1">
              <Plus class="h-3.5 w-3.5" /> Tambah Kategori
            </button>
          </div>

          <!-- HTML5 Draggable categories list -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div 
              v-for="(cat, idx) in categoryList"
              :key="cat.id"
              draggable="true"
              @dragstart="onCategoryDragStart(idx)"
              @dragover="onCategoryDragOver"
              @drop="onCategoryDrop(idx)"
              class="bg-card border rounded-xl p-4 hover:shadow-md transition-all flex flex-col justify-between cursor-move"
            >
              <div class="flex items-start justify-between mb-3">
                <div class="flex items-center gap-2.5">
                  <span class="text-muted-foreground"><GripVertical class="h-4.5 w-4.5 shrink-0" /></span>
                  <span class="text-xl leading-none">{{ cat.icon }}</span>
                  <div>
                    <h4 class="font-bold text-sm text-foreground">{{ cat.name }}</h4>
                    <p class="text-[10px] text-muted-foreground">{{ getProductsCountForCategory(cat.id) }} produk</p>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] font-semibold">Aktif</span>
              </div>
              <div class="flex items-center gap-2 mt-2">
                <span v-if="cat.webstore" class="px-1.5 py-0.5 rounded bg-muted text-muted-foreground text-[8px] font-bold uppercase tracking-wider">Webstore</span>
                <span v-if="cat.reseller" class="px-1.5 py-0.5 rounded bg-muted text-muted-foreground text-[8px] font-bold uppercase tracking-wider">Reseller</span>
                <span v-if="cat.pos" class="px-1.5 py-0.5 rounded bg-muted text-muted-foreground text-[8px] font-bold uppercase tracking-wider">POS</span>
              </div>
              <div class="flex gap-2 border-t mt-4 pt-3">
                <button @click="openCategoryForm(cat)" class="flex-1 h-7 border hover:bg-muted text-foreground text-xs font-semibold rounded flex items-center justify-center gap-1">
                  <Pencil class="h-3 w-3" /> Edit
                </button>
                <button @click="confirmDeleteCategory(cat)" class="flex-1 h-7 hover:bg-destructive/10 text-destructive text-xs font-semibold rounded flex items-center justify-center gap-1">
                  <Trash2 class="h-3 w-3" /> Hapus
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Product Manager -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-base text-foreground flex items-center gap-2">
                <PackagePlus class="h-4.5 w-4.5 text-muted-foreground" />
                Manajemen Produk
              </h3>
              <p class="text-xs text-muted-foreground mt-0.5">Tambah, edit, atau hapus produk yang ditampilkan di semua channel.</p>
            </div>
            <button @click="openProductForm(null)" class="h-8 px-3 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs transition-all flex items-center gap-1">
              <Plus class="h-3.5 w-3.5" /> Tambah Produk
            </button>
          </div>

          <!-- Product Filters -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full">
            <div class="relative flex-1">
              <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Cari nama atau SKU..." 
                v-model="settingsSearch"
                class="pl-8 h-9 w-full bg-card border rounded-lg text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" 
              />
            </div>
            <select v-model="settingsCategory" class="h-9 px-3 bg-card border rounded-lg text-xs focus:outline-none cursor-pointer">
              <option value="Semua">Semua Kategori</option>
              <option v-for="c in categoryList" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
            </select>
            <select v-model="settingsStatus" class="h-9 px-3 bg-card border rounded-lg text-xs focus:outline-none cursor-pointer">
              <option value="Semua">Semua Status</option>
              <option value="synced">✓ Aktif</option>
              <option value="syncing">⟳ Sync</option>
              <option value="out">✕ Habis</option>
            </select>
          </div>

          <!-- Products list with Draggable handles -->
          <div class="bg-card border rounded-xl overflow-hidden shadow-sm">
            <div class="overflow-x-auto">
              <table class="w-full text-sm text-left">
                <thead>
                  <tr class="border-b bg-muted/40 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    <th class="w-8 py-3.5 px-2"></th>
                    <th class="py-3.5 px-4">Produk</th>
                    <th class="py-3.5 px-4">SKU</th>
                    <th class="py-3.5 px-4">Kategori</th>
                    <th class="py-3.5 px-4 text-right">Harga</th>
                    <th class="py-3.5 px-4 text-right">Stok</th>
                    <th class="py-3.5 px-4 text-center">Channels</th>
                    <th class="py-3.5 px-4 text-center">Status</th>
                    <th class="py-3.5 px-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-border">
                  <tr 
                    v-for="(p, idx) in filteredSettingsProducts" 
                    :key="p.id"
                    draggable="true"
                    @dragstart="onProductDragStart(idx)"
                    @dragover="onProductDragOver"
                    @drop="onProductDrop(idx)"
                    class="hover:bg-muted/10 transition-colors"
                  >
                    <td class="py-3 px-2 text-center text-muted-foreground cursor-move">
                      <GripVertical class="h-4 w-4 mx-auto shrink-0" />
                    </td>
                    <td class="py-3 px-4">
                      <div class="flex items-center gap-3">
                        <img :src="p.img" :alt="p.name" class="h-9 w-9 rounded-lg object-cover bg-muted shrink-0" />
                        <div>
                          <p class="font-bold text-foreground text-xs sm:text-sm leading-tight">{{ p.name }}</p>
                          <p class="text-[10px] text-muted-foreground line-clamp-1 max-w-[200px] mt-0.5">{{ p.description }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="py-3 px-4 font-mono text-xs text-muted-foreground">{{ p.sku }}</td>
                    <td class="py-3 px-4 text-xs font-semibold">
                      <span class="px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                        {{ categoryLabel(p.category) }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-right font-bold text-foreground">{{ formatRp(p.price) }}</td>
                    <td class="py-3 px-4 text-right text-foreground">{{ p.stock }}</td>
                    <td class="py-3 px-4">
                      <div class="flex items-center justify-center gap-1">
                        <span v-if="p.ch_webstore" class="px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground text-[8px] font-bold uppercase">Web</span>
                        <span v-if="p.ch_pos" class="px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground text-[8px] font-bold uppercase">POS</span>
                        <span v-if="p.ch_reseller" class="px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground text-[8px] font-bold uppercase">Reseller</span>
                      </div>
                    </td>
                    <td class="py-3 px-4 text-center">
                      <span 
                        :class="[
                          'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold leading-none',
                          p.status === 'synced' ? 'bg-primary/10 text-primary' :
                          p.status === 'syncing' ? 'bg-amber-500/10 text-amber-500' : 'bg-destructive/10 text-destructive'
                        ]"
                      >
                        {{ p.status === 'synced' ? '✓ Aktif' : p.status === 'syncing' ? '⟳ Sync' : '✕ Habis' }}
                      </span>
                    </td>
                    <td class="py-3 px-4">
                      <div class="flex items-center justify-center gap-1.5">
                        <button @click="openProductForm(p)" class="p-1 rounded-md border hover:bg-muted text-foreground focus:outline-none transition-colors">
                          <Pencil class="h-3.5 w-3.5" />
                        </button>
                        <button @click="confirmDeleteProduct(p)" class="p-1 rounded-md hover:bg-destructive/10 text-destructive focus:outline-none transition-colors">
                          <Trash2 class="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── POPUP MODALS ──────────────────── -->
    <!-- 1. Category Form Modal -->
    <div v-if="showCategoryModal" class="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-card w-full max-w-md border rounded-2xl shadow-xl overflow-hidden animate-scale-in">
        <div class="px-5 py-4 border-b">
          <h3 class="font-bold text-base text-foreground">
            {{ categoryFormObj.id ? "Edit Kategori" : "Tambah Kategori" }}
          </h3>
        </div>
        <div class="p-5 space-y-4">
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-muted-foreground">ID Kategori (Unique) *</label>
            <input 
              type="text" 
              placeholder="e.g. Tops, Bottoms, Accessories" 
              v-model="categoryFormObj.id"
              :disabled="categoryFormObj.isEditing"
              class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20 disabled:bg-muted disabled:text-muted-foreground"
            />
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-muted-foreground">Nama Kategori *</label>
            <input 
              type="text" 
              placeholder="e.g. Atasan, Bawahan, Aksesoris" 
              v-model="categoryFormObj.name"
              class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20"
            />
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-muted-foreground">Icon Emoji</label>
            <input 
              type="text" 
              placeholder="e.g. 👕, 👖, 🎒" 
              v-model="categoryFormObj.icon"
              class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20"
            />
          </div>
          <div class="space-y-3 pt-2">
            <label class="text-xs font-semibold text-muted-foreground">Saluran Penjualan</label>
            <div class="flex gap-4">
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="categoryFormObj.webstore" class="rounded border-border focus:ring-0 text-primary" />
                Webstore
              </label>
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="categoryFormObj.reseller" class="rounded border-border focus:ring-0 text-primary" />
                Reseller
              </label>
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="categoryFormObj.pos" class="rounded border-border focus:ring-0 text-primary" />
                POS Kasir
              </label>
            </div>
          </div>
        </div>
        <div class="px-5 py-3.5 bg-muted/20 border-t flex justify-end gap-2">
          <button @click="showCategoryModal = false" class="h-9 px-4 rounded-lg bg-card border hover:bg-muted text-xs font-semibold transition-all">Batal</button>
          <button @click="saveCategory" class="h-9 px-4 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm">Simpan</button>
        </div>
      </div>
    </div>

    <!-- 2. Product Form Modal -->
    <div v-if="showProductModal" class="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-card w-full max-w-lg border rounded-2xl shadow-xl overflow-hidden animate-scale-in max-h-[90vh] overflow-y-auto">
        <div class="px-5 py-4 border-b">
          <h3 class="font-bold text-base text-foreground">
            {{ productFormObj.id ? "Edit Produk" : "Tambah Produk" }}
          </h3>
        </div>
        <div class="p-5 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">Nama Produk *</label>
              <input type="text" placeholder="Kaos Polos Premium" v-model="productFormObj.name" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">SKU *</label>
              <input type="text" placeholder="KPP-001" v-model="productFormObj.sku" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">Harga (IDR) *</label>
              <input type="number" placeholder="89000" v-model="productFormObj.price" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">Stok Fisik *</label>
              <input type="number" placeholder="100" v-model="productFormObj.stock" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">Kategori *</label>
              <select v-model="productFormObj.category" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none cursor-pointer">
                <option v-for="c in categoryList" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
              </select>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-muted-foreground">Image URL</label>
              <input type="text" placeholder="/products/product-kaos.png" v-model="productFormObj.img" class="h-9 w-full bg-card border rounded-lg px-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20" />
            </div>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-muted-foreground">Deskripsi Produk</label>
            <textarea placeholder="Tulis spesifikasi produk..." v-model="productFormObj.description" rows="3" class="w-full bg-card border rounded-lg p-3 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20"></textarea>
          </div>
          <div class="space-y-3 pt-2">
            <label class="text-xs font-semibold text-muted-foreground">Saluran Penjualan</label>
            <div class="flex gap-4">
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="productFormObj.ch_webstore" class="rounded border-border focus:ring-0 text-primary" />
                Webstore
              </label>
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="productFormObj.ch_pos" class="rounded border-border focus:ring-0 text-primary" />
                POS
              </label>
              <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                <input type="checkbox" v-model="productFormObj.ch_reseller" class="rounded border-border focus:ring-0 text-primary" />
                Reseller
              </label>
            </div>
          </div>
        </div>
        <div class="px-5 py-3.5 bg-muted/20 border-t flex justify-end gap-2">
          <button @click="showProductModal = false" class="h-9 px-4 rounded-lg bg-card border hover:bg-muted text-xs font-semibold transition-all">Batal</button>
          <button @click="saveProduct" class="h-9 px-4 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm">Simpan</button>
        </div>
      </div>
    </div>

    <!-- 3. POS Cashier Checkout Payment Dialog -->
    <div v-if="showPOSCheckoutModal" class="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-card w-full max-w-md border rounded-2xl shadow-xl overflow-hidden animate-scale-in">
        <div class="px-5 py-4 border-b flex justify-between items-center">
          <h3 class="font-bold text-base text-foreground flex items-center gap-2">
            <CreditCard class="h-4 w-4 text-primary" />
            Kasir Pembayaran
          </h3>
          <span class="text-xs bg-muted px-2 py-0.5 rounded font-mono">{{ selectedPaymentMethod.toUpperCase() }}</span>
        </div>
        <div class="p-5 space-y-4">
          <div class="flex justify-between items-center bg-muted/30 border rounded-xl p-4">
            <span class="text-sm font-semibold text-muted-foreground">Total Tagihan</span>
            <span class="text-xl font-bold text-primary">{{ formatRp(cartTotal) }}</span>
          </div>

          <div class="space-y-1.5" v-if="selectedPaymentMethod === 'cash'">
            <label class="text-xs font-semibold text-muted-foreground">Jumlah Uang Diterima (Cash)</label>
            <input 
              type="number" 
              v-model="cashReceived" 
              placeholder="Masukkan nominal bayar..."
              class="h-11 w-full bg-card border rounded-xl px-4 text-sm focus:outline-none focus:ring-1 focus:ring-primary/20 text-foreground font-bold"
            />
          </div>

          <!-- Quick Cash Suggestions -->
          <div class="flex gap-2 flex-wrap" v-if="selectedPaymentMethod === 'cash'">
            <button 
              v-for="amt in cashSuggestions" 
              :key="amt" 
              @click="cashReceived = amt"
              class="h-7 px-3 bg-muted/60 hover:bg-muted text-foreground text-xs font-semibold rounded-md border"
            >
              {{ formatRp(amt) }}
            </button>
          </div>

          <div class="flex justify-between items-center bg-muted/10 border border-dashed rounded-xl p-4 text-sm" v-if="selectedPaymentMethod === 'cash' && cashReceived > 0">
            <span class="font-semibold text-muted-foreground">Uang Kembali (Kembalian)</span>
            <span :class="['font-bold text-base', cashChange >= 0 ? 'text-success' : 'text-destructive']">
              {{ cashChange >= 0 ? formatRp(cashChange) : 'Uang Kurang' }}
            </span>
          </div>

          <div class="flex items-start gap-2 p-3 rounded-lg bg-accent/30 border text-xs text-muted-foreground" v-if="selectedPaymentMethod !== 'cash'">
            <QrCode class="h-4 w-4 text-primary mt-0.5 shrink-0" v-if="selectedPaymentMethod === 'qris'" />
            <CreditCard class="h-4 w-4 text-primary mt-0.5 shrink-0" v-else />
            <span>Mohon selesaikan transaksi non-tunai di terminal EDC / scanner QRIS. Setelah pembayaran diverifikasi, klik tombol Selesaikan Transaksi di bawah.</span>
          </div>
        </div>
        <div class="px-5 py-3.5 bg-muted/20 border-t flex justify-end gap-2">
          <button @click="showPOSCheckoutModal = false" class="h-9 px-4 rounded-lg bg-card border hover:bg-muted text-xs font-semibold transition-all">Batal</button>
          <button 
            @click="submitPOSOrder" 
            :disabled="selectedPaymentMethod === 'cash' && cashChange < 0"
            class="h-9 px-4 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-xs transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Selesaikan Transaksi
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import axios from "axios";
import {
  Store,
  ShoppingCart,
  Package,
  RefreshCw,
  Search,
  Star,
  Plus,
  Minus,
  Trash2,
  CreditCard,
  Banknote,
  QrCode,
  BarChart3,
  ArrowUpRight,
  Eye,
  ShoppingBag,
  Smartphone,
  Copy,
  Check,
  ExternalLink,
  Users,
  Percent,
  Link as LinkIcon,
  GripVertical,
  Settings,
  ArrowUpDown,
  Pencil,
  FolderPlus,
  PackagePlus,
  ChevronRight
} from "lucide-vue-next";

// Define Types
interface CategoryItem {
  id: string;
  name: string;
  icon: string;
  webstore: boolean;
  reseller: boolean;
  pos: boolean;
}

interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock: number;
  online: number;
  status: "synced" | "syncing" | "out";
  img: string;
  rating: number;
  sold: number;
  category: string;
  description: string;
  ch_webstore: boolean;
  ch_reseller: boolean;
  ch_pos: boolean;
}

interface StoreInfo {
  slug: string;
  name: string;
  owner: string;
  logo?: string;
  whatsapp: string;
  tagline: string;
  is_reseller: boolean;
  markup: number;
}

interface CartItem {
  id: number;
  product: Product;
  qty: number;
}

const tabsList = [
  { label: "Toko Saya", value: "mystore", icon: LinkIcon },
  { label: "Reseller", value: "resellers", icon: Users },
  { label: "POS Kasir", value: "pos", icon: Store },
  { label: "Inventori", value: "inventory", icon: Package },
  { label: "Pengaturan", value: "settings", icon: Settings },
];

const sortLabels = {
  default: "Default",
  price_asc: "Harga Terendah",
  price_desc: "Harga Tertinggi",
  bestseller: "Terlaris",
  rating: "Rating Tertinggi",
};

type SortOption = keyof typeof sortLabels;

// Data state
const activeTab = ref("mystore");
const aiManager = ref(true);
const products = ref<Product[]>([]);
const categoryList = ref<CategoryItem[]>([]);
const ownerStore = ref<StoreInfo>({
  slug: "urbanstyle-id",
  name: "UrbanStyle Indonesia",
  owner: "Andi Rahmawan",
  whatsapp: "6281234567890",
  tagline: "Fashion streetwear berkualitas untuk semua.",
  is_reseller: false,
  markup: 0
});
const resellerStores = ref<StoreInfo[]>([]);

// Page filters
const storeSort = ref<SortOption>("default");
const selectedCategory = ref("Semua");
const copiedLink = ref<string | null>(null);

// POS state
const posSearch = ref("");
const posCategory = ref("Semua");
const posSort = ref<SortOption>("default");
const cart = ref<CartItem[]>([]);
const selectedPaymentMethod = ref("cash");
const showPOSCheckoutModal = ref(false);
const cashReceived = ref<number>(0);
const cashSuggestions = ref<number[]>([]);

// Settings state
const settingsSearch = ref("");
const settingsCategory = ref("Semua");
const settingsStatus = ref("Semua");

// Modals forms
const showCategoryModal = ref(false);
const categoryFormObj = ref({
  id: "",
  name: "",
  icon: "📦",
  webstore: true,
  reseller: true,
  pos: true,
  isEditing: false
});

const showProductModal = ref(false);
const productFormObj = ref({
  id: 0,
  name: "",
  sku: "",
  price: 0,
  stock: 0,
  category: "",
  img: "",
  description: "",
  ch_webstore: true,
  ch_reseller: true,
  ch_pos: true
});

const channels = [
  { name: "Shopee", orders: 128, revenue: "Rp 24.5M", icon: "🟠" },
  { name: "Tokopedia", orders: 96, revenue: "Rp 18.2M", icon: "🟢" },
  { name: "TikTok Shop", orders: 74, revenue: "Rp 12.8M", icon: "⚫" },
  { name: "Offline POS", orders: 213, revenue: "Rp 38.1M", icon: "🏪" },
];

const posPaymentMethods = [
  { id: "cash", label: "Tunai", icon: Banknote },
  { id: "card", label: "EDC Kartu", icon: CreditCard },
  { id: "qris", label: "QRIS", icon: QrCode },
];

// Helper calculations
const formatRp = (n: number) => `Rp ${n.toLocaleString("id-ID")}`;
const storeUrl = (slug: string) => `${window.location.origin}/store/${slug}`;
const categoryLabel = (catId: string) => {
  const cat = categoryList.value.find((c) => c.id === catId);
  return cat ? `${cat.icon} ${cat.name}` : catId;
};
const activeProductsCount = computed(() => products.value.filter((p) => p.status === "synced").length);

const getProductsCountForCategory = (catId: string) => {
  return products.value.filter((p) => p.category === catId).length;
};

// API calls
const loadData = async () => {
  try {
    const prodRes = await axios.get("/api/products");
    products.value = prodRes.data;

    const catRes = await axios.get("/api/categories");
    categoryList.value = catRes.data;

    const storeRes = await axios.get("/api/stores");
    const allStores = storeRes.data;
    const owner = allStores.find((s: any) => !s.is_reseller);
    const resellers = allStores.filter((s: any) => s.is_reseller);
    if (owner) ownerStore.value = owner;
    if (resellers) resellerStores.value = resellers;
  } catch (error) {
    console.error("Error loading webstore data:", error);
  }
};

onMounted(() => {
  loadData();
});

// Category and product actions
const copyLink = (slug: string) => {
  navigator.clipboard.writeText(storeUrl(slug));
  copiedLink.value = slug;
  setTimeout(() => {
    copiedLink.value = null;
  }, 2000);
};

// Sort algorithm helper
const getSortedProducts = (list: Product[], sortBy: SortOption) => {
  const sorted = [...list];
  if (sortBy === "price_asc") return sorted.sort((a, b) => a.price - b.price);
  if (sortBy === "price_desc") return sorted.sort((a, b) => b.price - a.price);
  if (sortBy === "bestseller") return sorted.sort((a, b) => b.sold - a.sold);
  if (sortBy === "rating") return sorted.sort((a, b) => b.rating - a.rating);
  return sorted;
};

// Webstore tab calculations
const filteredWebstoreProducts = computed(() => {
  const list = products.value.filter(
    (p) =>
      p.ch_webstore &&
      p.status !== "out" &&
      (selectedCategory.value === "Semua" || p.category === selectedCategory.value)
  );
  return getSortedProducts(list, storeSort.value);
});

// POS tab calculations
const posFilteredProducts = computed(() => {
  const list = products.value.filter(
    (p) =>
      p.ch_pos &&
      p.stock > 0 &&
      (posCategory.value === "Semua" || p.category === posCategory.value) &&
      (p.name.toLowerCase().includes(posSearch.value.toLowerCase()) ||
        p.sku.toLowerCase().includes(posSearch.value.toLowerCase()))
  );
  return getSortedProducts(list, posSort.value);
});

// POS Cart handlers
const addToCart = (prodId: number) => {
  const p = products.value.find((pr) => pr.id === prodId);
  if (!p) return;
  
  const existing = cart.value.find((item) => item.id === prodId);
  if (existing) {
    if (existing.qty < p.stock) {
      existing.qty++;
    } else {
      alert(`Stok produk terbatas! Stok tersedia: ${p.stock}`);
    }
  } else {
    cart.value.push({
      id: prodId,
      product: p,
      qty: 1
    });
  }
};

const updateCartQty = (prodId: number, amt: number) => {
  const item = cart.value.find((i) => i.id === prodId);
  if (!item) return;
  const newQty = item.qty + amt;
  if (newQty <= 0) {
    removeCartItem(prodId);
  } else if (newQty <= item.product.stock) {
    item.qty = newQty;
  } else {
    alert(`Stok produk terbatas! Stok tersedia: ${item.product.stock}`);
  }
};

const removeCartItem = (prodId: number) => {
  cart.value = cart.value.filter((item) => item.id !== prodId);
};

const cartCount = computed(() => cart.value.reduce((s, i) => s + i.qty, 0));
const cartSubtotal = computed(() => cart.value.reduce((s, i) => s + i.product.price * i.qty, 0));
const cartTax = computed(() => Math.round(cartSubtotal.value * 0.11));
const cartTotal = computed(() => cartSubtotal.value + cartTax.value);

// Cash change calculation
const cashChange = computed(() => {
  return cashReceived.value - cartTotal.value;
});

// Quick cash suggestions based on total
watch(cartTotal, (newTotal) => {
  if (newTotal <= 0) {
    cashSuggestions.value = [];
    return;
  }
  const next50k = Math.ceil(newTotal / 50000) * 50000;
  const next100k = Math.ceil(newTotal / 100000) * 100000;
  
  const suggestions = new Set([
    newTotal,
    next50k,
    next100k,
    50000,
    100000,
    200000
  ]);
  
  cashSuggestions.value = Array.from(suggestions)
    .filter((v) => v >= newTotal)
    .sort((a, b) => a - b)
    .slice(0, 4);
});

// Checkout popup
const openCheckoutModal = () => {
  cashReceived.value = cartTotal.value;
  showPOSCheckoutModal.value = true;
};

const submitPOSOrder = async () => {
  try {
    // Post Order payload to Backend API
    const payload = {
      store_slug: ownerStore.value.slug,
      customer_name: "POS Walk-in Customer",
      customer_phone: "080000000000",
      address: "Walk-in Cashier Counter",
      city: "Offline Store Counter",
      shipping_method: "Pickup",
      shipping_courier: "POS Counter",
      shipping_cost: 0,
      payment_method: selectedPaymentMethod.value === "cash" 
        ? "Tunai (Cashier)" 
        : selectedPaymentMethod.value === "card" 
        ? "EDC Kartu" 
        : "QRIS",
      items: cart.value.map((i) => ({
        product_id: i.id,
        qty: i.qty,
        price: i.product.price
      }))
    };

    const res = await axios.post("/api/orders", payload);
    const order = res.data;

    // Immediately mark order as paid & completed
    await axios.put(`/api/orders/${order.id}/status`, {
      status: "paid"
    });
    await axios.put(`/api/orders/${order.id}/status`, {
      status: "delivered"
    });

    alert("Transaksi Kasir POS Berhasil dan Disimpan!");
    cart.value = [];
    showPOSCheckoutModal.value = false;
    loadData(); // reload inventory levels
  } catch (error: any) {
    console.error(error);
    alert(error.response?.data?.detail || "Gagal memproses transaksi kasir.");
  }
};

const syncAllProducts = () => {
  alert("Menyinkronkan stok inventori di Tokopedia, Shopee, dan TikTok Shop...");
};

// Resellers Actions
const addReseller = () => {
  alert("Fitur pendaftaran Reseller Partner. Sistem akan mengirim link pendaftaran.");
};

// HTML5 native drag and drop index tracks
const dragIndexCategory = ref<number | null>(null);
const onCategoryDragStart = (idx: number) => {
  dragIndexCategory.value = idx;
};
const onCategoryDragOver = (e: DragEvent) => {
  e.preventDefault();
};
const onCategoryDrop = (idx: number) => {
  if (dragIndexCategory.value !== null && dragIndexCategory.value !== idx) {
    const temp = categoryList.value[dragIndexCategory.value];
    categoryList.value.splice(dragIndexCategory.value, 1);
    categoryList.value.splice(idx, 0, temp);
  }
};

// Category Forms
const openCategoryForm = (cat: CategoryItem | null) => {
  if (cat) {
    categoryFormObj.value = {
      id: cat.id,
      name: cat.name,
      icon: cat.icon,
      webstore: cat.webstore,
      reseller: cat.reseller,
      pos: cat.pos,
      isEditing: true
    };
  } else {
    categoryFormObj.value = {
      id: "",
      name: "",
      icon: "📦",
      webstore: true,
      reseller: true,
      pos: true,
      isEditing: false
    };
  }
  showCategoryModal.value = true;
};

const saveCategory = async () => {
  if (!categoryFormObj.value.id || !categoryFormObj.value.name) {
    alert("Mohon isi ID dan Nama kategori!");
    return;
  }
  try {
    const payload = {
      id: categoryFormObj.value.id,
      name: categoryFormObj.value.name,
      icon: categoryFormObj.value.icon,
      webstore: categoryFormObj.value.webstore,
      reseller: categoryFormObj.value.reseller,
      pos: categoryFormObj.value.pos
    };

    if (categoryFormObj.value.isEditing) {
      // Direct delete and recreate or update (since API has POST / DELETE categories, let's post)
      // Actually we delete then post
      await axios.delete(`/api/categories/${payload.id}`);
      await axios.post("/api/categories", payload);
    } else {
      await axios.post("/api/categories", payload);
    }
    showCategoryModal.value = false;
    loadData();
  } catch (error) {
    console.error(error);
    alert("Gagal menyimpan kategori.");
  }
};

const confirmDeleteCategory = async (cat: CategoryItem) => {
  if (confirm(`Apakah Anda yakin ingin menghapus kategori ${cat.name}?`)) {
    try {
      await axios.delete(`/api/categories/${cat.id}`);
      loadData();
    } catch (error) {
      console.error(error);
      alert("Gagal menghapus kategori.");
    }
  }
};

// Settings product tab calculations
const filteredSettingsProducts = computed(() => {
  const list = products.value.filter((p) => {
    const matchSearch =
      !settingsSearch.value ||
      p.name.toLowerCase().includes(settingsSearch.value.toLowerCase()) ||
      p.sku.toLowerCase().includes(settingsSearch.value.toLowerCase());
    const matchCategory =
      settingsCategory.value === "Semua" || p.category === settingsCategory.value;
    const matchStatus =
      settingsStatus.value === "Semua" ||
      (settingsStatus.value === "synced" && p.status === "synced") ||
      (settingsStatus.value === "syncing" && p.status === "syncing") ||
      (settingsStatus.value === "out" && p.status === "out");
    return matchSearch && matchCategory && matchStatus;
  });
  return list;
});

// HTML5 native drag and drop index tracks for products
const dragIndexProduct = ref<number | null>(null);
const onProductDragStart = (idx: number) => {
  dragIndexProduct.value = idx;
};
const onProductDragOver = (e: DragEvent) => {
  e.preventDefault();
};
const onProductDrop = (idx: number) => {
  if (dragIndexProduct.value !== null && dragIndexProduct.value !== idx) {
    const temp = products.value[dragIndexProduct.value];
    products.value.splice(dragIndexProduct.value, 1);
    products.value.splice(idx, 0, temp);
  }
};

// Product Forms
const openProductForm = (p: Product | null) => {
  if (p) {
    productFormObj.value = {
      id: p.id,
      name: p.name,
      sku: p.sku,
      price: p.price,
      stock: p.stock,
      category: p.category,
      img: p.img,
      description: p.description,
      ch_webstore: p.ch_webstore,
      ch_reseller: p.ch_reseller,
      ch_pos: p.ch_pos
    };
  } else {
    productFormObj.value = {
      id: 0,
      name: "",
      sku: "",
      price: 0,
      stock: 0,
      category: categoryList.value[0]?.id || "Tops",
      img: "/products/product-kaos.png",
      description: "",
      ch_webstore: true,
      ch_reseller: true,
      ch_pos: true
    };
  }
  showProductModal.value = true;
};

const saveProduct = async () => {
  if (!productFormObj.value.name || !productFormObj.value.sku || !productFormObj.value.price) {
    alert("Mohon isi Nama, SKU, dan Harga produk!");
    return;
  }
  try {
    const payload = {
      name: productFormObj.value.name,
      sku: productFormObj.value.sku,
      price: Number(productFormObj.value.price),
      stock: Number(productFormObj.value.stock),
      online: Number(productFormObj.value.stock),
      status: Number(productFormObj.value.stock) > 0 ? "synced" : "out",
      img: productFormObj.value.img,
      category: productFormObj.value.category,
      description: productFormObj.value.description,
      ch_webstore: productFormObj.value.ch_webstore,
      ch_reseller: productFormObj.value.ch_reseller,
      ch_pos: productFormObj.value.ch_pos
    };

    if (productFormObj.value.id > 0) {
      await axios.put(`/api/products/${productFormObj.value.id}`, payload);
    } else {
      await axios.post("/api/products", payload);
    }
    showProductModal.value = false;
    loadData();
  } catch (error: any) {
    console.error(error);
    alert(error.response?.data?.detail || "Gagal menyimpan produk.");
  }
};

const confirmDeleteProduct = async (p: Product) => {
  if (confirm(`Apakah Anda yakin ingin menghapus produk ${p.name}?`)) {
    try {
      await axios.delete(`/api/products/${p.id}`);
      loadData();
    } catch (error) {
      console.error(error);
      alert("Gagal menghapus produk.");
    }
  }
};
</script>
