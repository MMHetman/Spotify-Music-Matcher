<template>
    <v-app>
        <app-nav />
        <v-main>
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

<style>
@import url('https://fonts.googleapis.com/css2?family=Ruda:wght@400;500;600;700;800;900&display=swap');
.v-application {
    font-family: 'Ruda', sans-serif !important;
}
</style>
