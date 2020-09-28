<template>
    <span>
        <v-app-bar color="grey darken-4" dark>
            <v-spacer class="hidden-md-and-up"></v-spacer>
            <router-link to="/">
                <v-toolbar-title data-cy="titleBtn">{{
                    appTitle
                }}</v-toolbar-title>
            </router-link>
            <v-spacer />
            <v-btn color="yellow darken-2" to="/about">About</v-btn>
        </v-app-bar>
    </span>
</template>

<script>
export default {
    name: 'AppNav',
    data() {
        return {
            appTitle: 'App name'
        };
    }
};
</script>

<style scoped>
a {
    color: white !important;
    text-decoration: none;
}
</style>