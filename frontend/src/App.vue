<template>
    <v-app>
        <app-nav />
        <v-main transition="slide-x-transition">
            <router-view></router-view>
        </v-main>
    </v-app>
</template>

<script>
import AppNav from '@/components/AppNav';
export default {
    name: 'App',
    components: { AppNav }
};
</script>

<style></style>
