<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-background p-6 text-center animate-fade-in">
    <div class="h-20 w-20 rounded-2xl bg-muted flex items-center justify-center text-muted-foreground mb-4">
      <AlertTriangle class="h-10 w-10 text-primary" />
    </div>
    <h1 class="text-3xl font-extrabold text-foreground tracking-tight mb-2">404</h1>
    <h2 class="text-lg font-bold text-foreground mb-2">Page Not Found</h2>
    <p class="text-muted-foreground text-sm max-w-md mb-6 leading-relaxed">
      Oops! The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
    </p>
    <router-link to="/">
      <button class="h-10 px-5 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center gap-1.5 focus:outline-none">
        <ArrowLeft class="h-4 w-4" /> Kembali ke Dashboard
      </button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { AlertTriangle, ArrowLeft } from "lucide-vue-next";
</script>
