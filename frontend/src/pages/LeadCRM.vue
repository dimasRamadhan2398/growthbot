<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Lead CRM</h1>
      <p class="text-muted-foreground text-sm mt-1">AI-captured leads across all your channels.</p>
    </div>

    <!-- Kanban Board Grid -->
    <div class="flex gap-4 overflow-x-auto pb-6 scrollbar-thin">
      <div 
        v-for="col in columns" 
        :key="col.title" 
        @dragover.prevent
        @drop="handleDrop($event, col.title)"
        class="flex-shrink-0 w-[300px] flex flex-col gap-3 rounded-xl bg-muted/40 p-4 border h-[calc(100vh-200px)] overflow-y-auto"
      >
        <!-- Column Header -->
        <div class="flex items-center gap-2 mb-2 sticky top-0 bg-muted/40 backdrop-blur-md pb-2 border-b">
          <span :class="['h-2.5 w-2.5 rounded-full', col.color]" />
          <h3 class="text-sm font-bold text-foreground">{{ col.title }}</h3>
          <span class="ml-auto px-2 py-0.5 rounded-full bg-card border text-[10px] font-bold text-muted-foreground">
            {{ getLeadsForColumn(col.title).length }}
          </span>
        </div>

        <!-- Kanban Cards -->
        <div class="space-y-2.5 flex-1">
          <div 
            v-for="lead in getLeadsForColumn(col.title)" 
            :key="lead.id"
            draggable="true"
            @dragstart="handleDragStart($event, lead.id)"
            class="bg-card border rounded-xl p-4 space-y-3 cursor-grab active:cursor-grabbing hover:shadow-md hover:border-primary/20 transition-all"
          >
            <div class="flex items-center gap-2.5">
              <div class="h-8 w-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-bold shrink-0">
                {{ lead.initials }}
              </div>
              <div class="min-w-0">
                <p class="text-xs sm:text-sm font-bold text-foreground truncate leading-none">{{ lead.name }}</p>
                <p class="text-[10px] text-muted-foreground mt-1">{{ lead.source }}</p>
              </div>
            </div>
            
            <div class="flex items-center justify-between border-t border-border/40 pt-2 text-xs">
              <span class="font-bold text-primary">{{ lead.value }}</span>
              <span class="text-[10px] text-muted-foreground">{{ lead.time }}</span>
            </div>

            <div class="flex gap-1.5 pt-1">
              <button @click="contactLead(lead.name, 'Chat')" class="flex-1 flex items-center justify-center gap-1 text-[11px] font-bold py-1.5 rounded-lg bg-secondary hover:bg-muted text-foreground transition-all focus:outline-none border shadow-sm">
                <MessageSquare class="h-3 w-3" /> Chat
              </button>
              <button @click="contactLead(lead.name, 'Call')" class="flex-1 flex items-center justify-center gap-1 text-[11px] font-bold py-1.5 rounded-lg bg-secondary hover:bg-muted text-foreground transition-all focus:outline-none border shadow-sm">
                <Phone class="h-3 w-3" /> Call
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { MessageSquare, Phone } from "lucide-vue-next";

interface Lead {
  id: number;
  name: string;
  initials: string;
  source: string;
  value: string;
  time: string;
  column_name: string;
}

const leads = ref<Lead[]>([]);

const columns = [
  { title: "New Lead", color: "bg-cyan-500" },
  { title: "Qualified by AI", color: "bg-indigo-500" },
  { title: "In Discussion", color: "bg-amber-500" },
  { title: "Closed", color: "bg-emerald-500" },
];

const loadLeads = async () => {
  try {
    const res = await axios.get("/api/leads");
    leads.value = res.data;
  } catch (error) {
    console.error("Error loading leads:", error);
  }
};

onMounted(() => {
  loadLeads();
});

const getLeadsForColumn = (colName: string) => {
  return leads.value.filter((l) => l.column_name === colName);
};

// Drag and drop events
const handleDragStart = (e: DragEvent, leadId: number) => {
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", leadId.toString());
  }
};

const handleDrop = async (e: DragEvent, columnName: string) => {
  e.preventDefault();
  if (e.dataTransfer) {
    const idStr = e.dataTransfer.getData("text/plain");
    if (!idStr) return;
    const leadId = parseInt(idStr);

    // Optimistic UI updates
    const targetLead = leads.value.find((l) => l.id === leadId);
    if (targetLead && targetLead.column_name !== columnName) {
      targetLead.column_name = columnName;

      try {
        await axios.put(`/api/leads/${leadId}`, {
          column_name: columnName
        });
      } catch (error) {
        console.error("Error updating lead column:", error);
        // rollback
        loadLeads();
      }
    }
  }
};

const contactLead = (name: string, method: string) => {
  alert(`Connecting to lead "${name}" via automated AI dialer (${method})...`);
};
</script>
