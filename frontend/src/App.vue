<template>
  <div class="min-h-screen bg-sepet-bg">
    <!-- Navbar -->
    <nav class="glass-card sticky top-0 z-50 rounded-none border-x-0 border-t-0">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-3">
            <span class="text-3xl">🐾</span>
            <div>
              <h1 class="text-lg font-bold text-sepet-primary-light tracking-tight">SEPET</h1>
              <p class="text-[10px] text-sepet-text-muted -mt-1">Sistema de Esterilização de Pets</p>
            </div>
          </div>
          <div class="flex gap-2">
            <router-link
              to="/"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300"
              :class="$route.path === '/' ? 'bg-sepet-primary text-white shadow-lg shadow-sepet-primary/30' : 'text-sepet-text-muted hover:text-white hover:bg-sepet-surface-light'"
            >
              📋 Agendamento
            </router-link>
            <router-link
              to="/gestao"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300"
              :class="$route.path === '/gestao' ? 'bg-sepet-secondary text-white shadow-lg shadow-sepet-secondary/30' : 'text-sepet-text-muted hover:text-white hover:bg-sepet-surface-light'"
            >
              🩺 Gestão
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </main>

    <!-- Footer -->
    <footer class="border-t border-sepet-surface-light/30 mt-auto">
      <div class="max-w-7xl mx-auto px-4 py-6 text-center text-xs text-sepet-text-muted">
        <p>📧 agendamento@sepet.am.gov.br · 📞 (92) 99207-1671</p>
        <p class="mt-1">📍 Av. Umberto Calderaro, 934 – Adrianópolis, Manaus-AM</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>
