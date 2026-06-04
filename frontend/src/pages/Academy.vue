<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Back to Course List Button -->
    <div v-if="selectedCourse" class="space-y-6">
      <button 
        @click="selectedCourseId = null" 
        class="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors focus:outline-none"
      >
        <ArrowLeft class="h-4 w-4" /> Back to courses
      </button>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main player section -->
        <div class="lg:col-span-2 space-y-4">
          <div class="aspect-video rounded-xl bg-slate-900 flex flex-col items-center justify-center border border-border shadow-inner relative overflow-hidden group">
            <!-- Mock Video Background Effect -->
            <div class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-transparent to-slate-950/40 pointer-events-none"></div>
            <div class="text-center space-y-3 z-10">
              <button 
                @click="playVideo" 
                class="mx-auto h-16 w-16 rounded-full bg-primary/10 hover:bg-primary/20 flex items-center justify-center transition-all duration-300 border border-primary/20 hover:scale-105"
              >
                <Play class="h-7 w-7 text-primary ml-1" />
              </button>
              <div>
                <p class="text-sm font-semibold text-slate-100">{{ selectedLessonTitle }}</p>
                <p class="text-xs text-slate-400 mt-1">Video Tutorial — {{ selectedCourse.title }}</p>
              </div>
            </div>
          </div>
          
          <h1 class="text-xl font-bold mt-2">{{ selectedCourse.title }}</h1>
          <p class="text-muted-foreground text-sm leading-relaxed">{{ selectedCourse.desc }}</p>
          
          <button 
            @click="deployTemplate" 
            class="h-11 px-6 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-sm transition-all shadow-sm flex items-center gap-2"
          >
            <Rocket class="h-4 w-4" /> Deploy this AI Template
          </button>
        </div>

        <!-- Lessons sidebar -->
        <div class="bg-card border rounded-xl p-4 shadow-sm space-y-3">
          <h3 class="font-bold text-sm text-foreground">Lessons</h3>
          <div class="space-y-1.5">
            <div 
              v-for="(lesson, idx) in lessonContent.slice(0, selectedCourse.lessons)" 
              :key="idx"
              @click="activeLessonIdx = idx"
              :class="[
                'flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors border',
                activeLessonIdx === idx 
                  ? 'bg-accent/60 border-primary/30 text-accent-foreground font-medium' 
                  : 'bg-card border-transparent hover:bg-muted/60 text-muted-foreground hover:text-foreground'
              ]"
            >
              <span 
                :class="[
                  'h-7 w-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 transition-colors',
                  activeLessonIdx === idx ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
                ]"
              >
                {{ idx + 1 }}
              </span>
              <span class="text-xs sm:text-sm">{{ lesson }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Course List View -->
    <div v-else class="space-y-6">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">AI Academy</h1>
        <p class="text-muted-foreground text-sm mt-1">
          Learn, then deploy. Every course connects directly to an AI template.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="c in courses" 
          :key="c.id" 
          @click="selectCourse(c.id)"
          class="bg-card border rounded-xl p-5 cursor-pointer hover:shadow-md transition-shadow group flex flex-col justify-between"
        >
          <div class="space-y-3">
            <div :class="['h-32 rounded-lg flex items-center justify-center border border-border/40', c.color]">
              <BookOpen class="h-10 w-10 text-muted-foreground/40" />
            </div>
            <span class="inline-flex px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground text-[10px] font-semibold">
              {{ c.level }}
            </span>
            <h3 class="font-bold text-base text-foreground group-hover:text-primary transition-colors leading-tight">
              {{ c.title }}
            </h3>
            <p class="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
              {{ c.desc }}
            </p>
          </div>
          <div class="flex items-center gap-4 text-[11px] text-muted-foreground pt-4 mt-4 border-t border-border/40">
            <span class="flex items-center gap-1">
              <BookOpen class="h-3.5 w-3.5" /> {{ c.lessons }} lessons
            </span>
            <span class="flex items-center gap-1">
              <Clock class="h-3.5 w-3.5" /> {{ c.duration }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { ArrowLeft, Play, Rocket, Clock, BookOpen } from "lucide-vue-next";

interface Course {
  id: number;
  title: string;
  desc: string;
  lessons: number;
  duration: string;
  level: string;
  color: string;
}

const courses: Course[] = [
  { id: 1, title: "WhatsApp AI Setup", desc: "Deploy a 24/7 AI sales assistant on WhatsApp Business in under 30 minutes.", lessons: 8, duration: "2h 15m", level: "Beginner", color: "bg-emerald-500/5 text-emerald-600" },
  { id: 2, title: "Inventory Automation", desc: "Sync your POS inventory across Shopee, Tokopedia, and TikTok Shop automatically.", lessons: 6, duration: "1h 45m", level: "Intermediate", color: "bg-blue-500/5 text-blue-600" },
  { id: 3, title: "AI Lead Qualification", desc: "Train your AI to qualify leads and route hot prospects to your sales team.", lessons: 5, duration: "1h 30m", level: "Intermediate", color: "bg-amber-500/5 text-amber-600" },
  { id: 4, title: "Smart Order Processing", desc: "Automate order confirmations, payment checks, and shipping notifications.", lessons: 7, duration: "2h", level: "Beginner", color: "bg-indigo-500/5 text-indigo-600" },
  { id: 5, title: "Customer Feedback AI", desc: "Collect, categorize, and respond to customer feedback at scale with AI.", lessons: 4, duration: "1h", level: "Beginner", color: "bg-rose-500/5 text-rose-600" },
  { id: 6, title: "Multi-Channel Campaigns", desc: "Launch coordinated marketing blasts across all your connected channels.", lessons: 9, duration: "3h", level: "Advanced", color: "bg-slate-500/5 text-slate-600" },
];

const lessonContent = [
  "Introduction & Prerequisites",
  "Setting Up Your API Connection",
  "Configuring AI Response Templates",
  "Training on Your Product Catalog",
  "Testing & Quality Assurance",
  "Going Live & Monitoring",
  "Advanced Customization",
  "Scaling & Optimization",
  "Post-Launch Analytics",
];

const selectedCourseId = ref<number | null>(null);
const activeLessonIdx = ref(0);

const selectedCourse = computed(() => {
  return courses.find((c) => c.id === selectedCourseId.value) || null;
});

const selectedLessonTitle = computed(() => {
  return lessonContent[activeLessonIdx.value] || "Tutorial Video";
});

const selectCourse = (id: number) => {
  selectedCourseId.value = id;
  activeLessonIdx.value = 0;
};

const playVideo = () => {
  alert(`Playing lesson video: "${selectedLessonTitle.value}"`);
};

const deployTemplate = () => {
  alert(`Deploying AI Template for "${selectedCourse.value?.title}" to your active agents!`);
};
</script>
