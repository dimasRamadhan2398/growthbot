<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">My AI Agents</h1>
      <p class="text-muted-foreground text-sm mt-1">Manage your AI workforce and knowledge base.</p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 3" :key="i" class="metric-card animate-pulse h-32 bg-card border"></div>
    </div>

    <!-- AI Agents Cards -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="a in agents" :key="a.name" class="bg-card border rounded-xl p-5 hover:shadow-md transition-shadow group flex flex-col justify-between">
        <div class="space-y-3">
          <div class="flex items-start justify-between">
            <div class="p-2.5 rounded-lg bg-primary/10 text-primary">
              <component :is="iconMap[a.icon_name]" class="h-5 w-5" />
            </div>
            <button 
              @click="toggleAgentStatus(a)"
              :class="[
                'px-2 py-0.5 rounded-full text-[10px] font-bold transition-all focus:outline-none border',
                a.status === 'active' 
                  ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' 
                  : 'bg-slate-500/10 text-slate-500 border-slate-500/20'
              ]"
            >
              {{ a.status === "active" ? "● Active" : "⏸ Paused" }}
            </button>
          </div>
          <div>
            <h3 class="font-bold text-sm text-foreground">{{ a.name }}</h3>
            <p class="text-xs text-muted-foreground mt-0.5">{{ a.channel }}</p>
          </div>
        </div>
        <div class="flex items-center justify-between pt-3 mt-4 border-t border-border/50">
          <span class="text-xs text-muted-foreground font-medium">
            {{ a.messages.toLocaleString() }} messages handled
          </span>
          <button @click="configureAgent(a.name)" class="text-xs h-7 px-2 hover:bg-muted text-foreground border rounded font-semibold transition-colors focus:outline-none">
            Configure
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Knowledge Base -->
      <div class="bg-card border rounded-xl p-5 shadow-sm space-y-4">
        <div class="flex items-center gap-2 border-b pb-3">
          <Database class="h-4.5 w-4.5 text-primary" />
          <h3 class="font-bold text-base text-foreground">Knowledge Base</h3>
        </div>
        
        <!-- Drag & Drop Uploader Area -->
        <div
          @dragover.prevent="dragOver = true"
          @dragleave="dragOver = false"
          @drop.prevent="handleFileDrop"
          :class="[
            'border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer',
            dragOver ? 'border-primary bg-accent/60' : 'border-border hover:bg-muted/10'
          ]"
          @click="triggerFileInput"
        >
          <!-- Hidden file input -->
          <input 
            type="file" 
            ref="fileInputRef" 
            class="hidden" 
            @change="handleFileSelect"
            accept=".pdf,.xlsx,.docx"
          />
          <Upload class="h-8 w-8 mx-auto text-muted-foreground mb-2" />
          <p class="text-sm font-semibold text-foreground">Drop files here or click to upload</p>
          <p class="text-xs text-muted-foreground mt-1">PDF, XLSX, DOCX up to 25MB</p>
        </div>

        <!-- Files list -->
        <div class="space-y-2">
          <div v-for="f in kbFiles" :key="f.name" class="flex items-center justify-between p-2.5 rounded-lg border bg-card hover:bg-muted/40 transition-colors">
            <div class="flex items-center gap-3 min-w-0">
              <FileText class="h-4 w-4 text-muted-foreground shrink-0" />
              <div class="min-w-0">
                <p class="text-sm font-semibold text-foreground truncate leading-snug">{{ f.name }}</p>
                <p class="text-[10px] text-muted-foreground mt-0.5">{{ f.size }} · {{ f.date }}</p>
              </div>
            </div>
            <button @click="deleteKbFile(f.id)" class="p-1 rounded-md text-destructive hover:bg-destructive/10 transition-colors focus:outline-none">
              <Trash2 class="h-4.5 w-4.5" />
            </button>
          </div>
        </div>
      </div>

      <!-- POS Integration Details -->
      <div class="bg-card border rounded-xl p-5 shadow-sm space-y-4">
        <div class="flex items-center gap-2 border-b pb-3">
          <ShoppingBag class="h-4.5 w-4.5 text-primary" />
          <h3 class="font-bold text-base text-foreground">POS Integration</h3>
        </div>
        
        <div class="p-4 rounded-xl bg-accent/30 border border-primary/10">
          <div class="flex items-center gap-2 mb-2">
            <span class="h-2.5 w-2.5 rounded-full bg-success" />
            <span class="text-sm font-bold text-foreground">Connected to POS Inventory</span>
          </div>
          <p class="text-xs text-muted-foreground leading-relaxed">
            Your AI agents can access real-time stock levels and product data from your POS system to assist customers 24/7.
          </p>
        </div>

        <div class="space-y-2.5 text-sm text-foreground">
          <div class="flex justify-between border-b pb-2">
            <span class="text-muted-foreground">Products synced</span>
            <span class="font-bold">529</span>
          </div>
          <div class="flex justify-between border-b pb-2">
            <span class="text-muted-foreground">Last sync</span>
            <span class="font-bold">2 minutes ago</span>
          </div>
          <div class="flex justify-between border-b pb-2">
            <span class="text-muted-foreground">Auto-reply enabled</span>
            <span class="font-bold text-success">Yes</span>
          </div>
          <div class="flex justify-between pb-1">
            <span class="text-muted-foreground">Out-of-stock handling</span>
            <span class="font-bold">Suggest alternatives</span>
          </div>
        </div>
        
        <button @click="managePOSConnection" class="w-full h-10 border rounded-lg hover:bg-muted text-foreground font-semibold text-xs transition-colors flex items-center justify-center gap-2 focus:outline-none">
          <Package class="h-4.5 w-4.5" /> Manage POS Connection
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import {
  Bot,
  Upload,
  Database,
  MessageSquare,
  ShoppingBag,
  Headphones,
  HelpCircle,
  FileText,
  Package,
  Trash2
} from "lucide-vue-next";

// Mapping icons to component
const iconMap = {
  MessageSquare,
  Headphones,
  ShoppingBag,
  HelpCircle,
  Package,
  Bot
};

interface Agent {
  id: number;
  name: string;
  status: "active" | "paused";
  messages: number;
  channel: string;
  icon_name: keyof typeof iconMap;
}

interface KBFile {
  id: number;
  name: string;
  size: string;
  date: string;
}

const agents = ref<Agent[]>([]);
const kbFiles = ref<KBFile[]>([]);
const isLoading = ref(true);
const dragOver = ref(false);
const fileInputRef = ref<HTMLInputElement | null>(null);

const loadData = async () => {
  try {
    const agentsRes = await axios.get("/api/agents");
    agents.value = agentsRes.data;

    const filesRes = await axios.get("/api/kb-files");
    kbFiles.value = filesRes.data;
  } catch (error) {
    console.error("Error loading agents data:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadData();
});

const toggleAgentStatus = async (agent: Agent) => {
  const nextStatus = agent.status === "active" ? "paused" : "active";
  try {
    const res = await axios.put(`/api/agents/${agent.id}`, {
      status: nextStatus
    });
    agent.status = res.data.status;
  } catch (error) {
    console.error("Error updating agent status:", error);
  }
};

const configureAgent = (name: string) => {
  alert(`Opening configuration panel for: "${name}"`);
};

// File uploading mock triggers
const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const uploadFile = async (name: string, sizeBytes: number) => {
  // Format size to human readable
  let size = "100 KB";
  if (sizeBytes >= 1048576) {
    size = `${(sizeBytes / 1048576).toFixed(1)} MB`;
  } else {
    size = `${(sizeBytes / 1024).toFixed(0)} KB`;
  }

  const payload = {
    name,
    size,
    date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
  };

  try {
    const res = await axios.post("/api/kb-files", payload);
    kbFiles.value.push(res.data);
  } catch (error) {
    console.error(error);
    alert("Gagal mengupload file ke knowledge base.");
  }
};

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    uploadFile(file.name, file.size);
  }
};

const handleFileDrop = (e: DragEvent) => {
  dragOver.value = false;
  if (e.dataTransfer && e.dataTransfer.files.length > 0) {
    const file = e.dataTransfer.files[0];
    uploadFile(file.name, file.size);
  }
};

const deleteKbFile = async (id: number) => {
  if (confirm("Hapus file ini dari knowledge base?")) {
    try {
      await axios.delete(`/api/kb-files/${id}`);
      kbFiles.value = kbFiles.value.filter((f) => f.id !== id);
    } catch (error) {
      console.error(error);
      alert("Gagal menghapus file.");
    }
  }
};

const managePOSConnection = () => {
  alert("Redirecting to POS Connection configurations...");
};
</script>
