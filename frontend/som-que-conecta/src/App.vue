<template>
  <div id="app" class="min-h-screen flex flex-col bg-gray-50">
    <AppNavbar />
    <main class="flex-grow container mx-auto px-4 py-8">
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import AppNavbar from './components/layout/AppNavbar.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>